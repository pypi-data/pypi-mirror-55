# -*- mode: python; coding: utf-8 -*
# Copyright (c) 2018 Radio Astronomy Software Group
# Licensed under the 3-clause BSD License

from __future__ import absolute_import, division, print_function

import numpy as np
import sys
import h5py

import six
from scipy.linalg import orthogonal_procrustes as ortho_procr

from astropy.coordinates import Angle, SkyCoord, EarthLocation, AltAz
from astropy.time import Time
import astropy_healpix

from . import utils as simutils
from . import spherical_coordinates_basis_transformation as scbt


def estimate_skymodel_memory_usage(Ncomponents, Nfreqs):
    """
    Estimate the memory footprint of a SkyModel by summing the sizes
    of the data types that go into SkyModel.

    This aims to anticipate the full memory required to handle a SkyModel
    class in simulation, accounting for its attributes as well as temporary
    and intermediate data.

    Parameters
    ----------

    Ncomponents : int
        Number of source components.
    Nfreqs : int
        Number of frequencies per source component.
        (size of SkyModel.freq_array)

    Returns
    -------
    mem_est : float
        Estimate of memory usage in bytes
    """

    base_float = [1.5]    # A float
    base_bool = [True]
    base_str = ["source_name"]

    Ncomp_attrs = {'ra': base_float, 'dec': base_float,
                   'alt_az': 2 * base_float, 'rise_lst': base_float, 'set_lst': base_float,
                   'pos_lmn': 3 * base_float, 'name': base_str, 'horizon_mask': base_bool}
    Ncomp_Nfreq_attrs = {'stokes': 4 * base_float,
                         'coherency_radec': 4 * base_float,
                         'coherency_local': 4 * base_float}

    mem_est = np.sum([sys.getsizeof(v) * Ncomponents for k, v in six.iteritems(Ncomp_attrs)])
    mem_est += np.sum([sys.getsizeof(v) * Ncomponents * Nfreqs
                       for k, v in six.iteritems(Ncomp_Nfreq_attrs)])
    return mem_est


class SkyModel(object):
    """
    Defines a set of point source components at given ICRS ra/dec coordinates, with a
    flux densities defined by stokes parameters.

    Used to calculate local coherency matrix for source brightness in AltAz
    frame at a specified time.

    Parameters
    ----------
    name : array_like of str
        Unique identifier for the source.
    ra : astropy Angle object
        source RA in J2000 (or ICRS) coordinates, shape (Ncomponents,).
    dec : astropy Angle object
        source Dec in J2000 (or ICRS) coordinates, shape (Ncomponents,).
    stokes : array_like of float
        4 element vector giving the source [I, Q, U, V], shape (4, Ncomponents).
    freq : astropy Quantity
        Reference frequencies of flux values, shape (Ncomponents,).
    rise_lst : array_like of float
        Approximate lst (radians) when the source rises, shape (Ncomponents,).
        Set by coarse horizon cut in simsetup.
        Default is nan, meaning the source never rises.
    set_lst : array_like of float
        Approximate lst (radians) when the source sets, shape (Ncomponents,).
        Default is None, meaning the source never sets.
    pos_tol : float
        position tolerance in degrees, defaults to minimum float in numpy
        position tolerance in degrees
    """

    Ncomponents = None  # Number of point source components represented here.

    _Ncomp_attrs = ['ra', 'dec', 'coherency_radec', 'coherency_local',
                    'stokes', 'alt_az', 'rise_lst', 'set_lst', 'freq',
                    'pos_lmn', 'name', 'horizon_mask']
    _scalar_attrs = ['Ncomponents', 'time', 'pos_tol']

    _member_funcs = ['coherency_calc', 'update_positions']

    def __init__(self, name, ra, dec, stokes,
                 Nfreqs=1, freq_array=None, rise_lst=None, set_lst=None,
                 spectral_type=None, pos_tol=np.finfo(float).eps):
        """
        Args:
            name: Unique identifier for the source.
            ra: astropy Angle object, shape (Ncomponents,)
                source RA in J2000 (or ICRS) coordinates
            dec: astropy Angle object, shape (Ncomponents,)
                source Dec in J2000 (or ICRS) coordinates
            stokes: shape (4, Nfreqs, Ncomponents)
                4 element vector giving the source [I, Q, U, V]
            Nfreqs: (integer)
                length of frequency axis
            freq_array: shape(Nfreqs,)
                corresponding frequencies for each flux density
            rise_lst: (float), shape (Ncomponents,)
                Approximate lst (radians) when the source rises.
                Set by coarse horizon cut in simsetup.
                Default is nan, meaning the source never rises.
            set_lst: (float), shape (Ncomponents,)
                Approximate lst (radians) when the source sets.
                Default is None, meaning the source never sets.
            pos_tol: float, defaults to minimum float in numpy
                position tolerance in degrees
        """

        if not isinstance(ra, Angle):
            raise ValueError('ra must be an astropy Angle object. '
                             'value was: {ra}'.format(ra=ra))

        if not isinstance(dec, Angle):
            raise ValueError('dec must be an astropy Angle object. '
                             'value was: {dec}'.format(dec=dec))

        self.Ncomponents = ra.size

        self.name = np.atleast_1d(np.asarray(name))
        self.freq_array = np.atleast_1d(freq_array)
        self.Nfreqs = Nfreqs
        self.stokes = np.asarray(stokes)
        self.ra = np.atleast_1d(ra)
        self.dec = np.atleast_1d(dec)
        self.pos_tol = pos_tol
        self.spectral_type = spectral_type

        self.has_rise_set_lsts = False
        if (rise_lst is not None) and (set_lst is not None):
            self.rise_lst = np.asarray(rise_lst)
            self.set_lst = np.asarray(set_lst)
            self.has_rise_set_lsts = True

        self.alt_az = np.zeros((2, self.Ncomponents), dtype=float)
        self.pos_lmn = np.zeros((3, self.Ncomponents), dtype=float)

        self.horizon_mask = np.zeros(self.Ncomponents).astype(
            bool)  # If true, source component is below horizon.

        # TODO -- Need a way of passing the spectral_type from catalog to each rank.
        # For now, if there are multiple frequencies, assume we have one per simulation frequency.
        if self.spectral_type is None:
            self.spectral_type = 'flat'
        if self.Nfreqs > 1:
            self.spectral_type = 'full'

        if self.Ncomponents == 1:
            self.stokes = self.stokes.reshape(4, Nfreqs, 1)

        # The coherency is a 2x2 matrix giving electric field correlation in Jy
        # Multiply by .5 to ensure that Trace sums to I not 2*I
        # Shape = (2,2,Ncomponents)

        self.coherency_radec = simutils.stokes_to_coherency(self.stokes)

        self.time = None

        assert np.all(
            [self.Ncomponents == l for l in [self.ra.size, self.dec.size, self.stokes.shape[2]]]
        ), 'Inconsistent quantity dimensions.'

    def _calc_average_rotation_matrix(self, telescope_location):
        """
        Calculate the "average" rotation matrix from RA/Dec to AltAz.

        This gets us close to the right value, then need to calculate a correction
        for each source separately.

        Parameters
        ----------
        telescope_location : astropy EarthLocation object
            Location of the telescope.

        Returns
        -------
        array of floats
            Rotation matrix that defines the average mapping (RA,Dec) <--> (Alt,Az),
            shape (3, 3).
        """
        # unit vectors to be transformed by astropy
        x_c = np.array([1., 0, 0])
        y_c = np.array([0, 1., 0])
        z_c = np.array([0, 0, 1.])

        # astropy 2 vs 3 use a different keyword name
        if six.PY2:
            rep_keyword = 'representation'
        else:
            rep_keyword = 'representation_type'

        rep_dict = {}
        rep_dict[rep_keyword] = 'cartesian'
        axes_icrs = SkyCoord(x=x_c, y=y_c, z=z_c, obstime=self.time,
                             location=telescope_location, frame='icrs',
                             **rep_dict)

        axes_altaz = axes_icrs.transform_to('altaz')
        setattr(axes_altaz, rep_keyword, 'cartesian')

        ''' This transformation matrix is generally not orthogonal
            to better than 10^-7, so let's fix that. '''

        R_screwy = axes_altaz.cartesian.xyz
        R_really_orthogonal, _ = ortho_procr(R_screwy, np.eye(3))

        # Note the transpose, to be consistent with calculation in scbt
        R_really_orthogonal = np.array(R_really_orthogonal).T

        return R_really_orthogonal

    def _calc_rotation_matrix(self, telescope_location):
        """
        Calculate the true rotation matrix from RA/Dec to AltAz for each component.

        Parameters
        ----------
        telescope_location : astropy EarthLocation object
            Location of the telescope.

        Returns
        -------
        array of floats
            Rotation matrix that defines the mapping (RA,Dec) <--> (Alt,Az),
            shape (3, 3, Ncomponents).
        """
        # Find mathematical points and vectors for RA/Dec
        theta_radec = np.pi / 2. - self.dec.rad
        phi_radec = self.ra.rad
        radec_vec = scbt.r_hat(theta_radec, phi_radec)
        assert radec_vec.shape == (3, self.Ncomponents)

        # Find mathematical points and vectors for Alt/Az
        theta_altaz = np.pi / 2. - self.alt_az[0, :]
        phi_altaz = self.alt_az[1, :]
        altaz_vec = scbt.r_hat(theta_altaz, phi_altaz)
        assert altaz_vec.shape == (3, self.Ncomponents)

        R_avg = self._calc_average_rotation_matrix(telescope_location)

        R_exact = np.zeros((3, 3, self.Ncomponents), dtype=np.float)
        for src_i in range(self.Ncomponents):
            intermediate_vec = np.matmul(R_avg, radec_vec[:, src_i])

            R_perturb = scbt.vecs2rot(r1=intermediate_vec, r2=altaz_vec[:, src_i])

            R_exact[:, :, src_i] = np.matmul(R_perturb, R_avg)

        return R_exact

    def _calc_coherency_rotation(self, telescope_location):
        """
        Calculate the rotation matrix to apply to the RA/Dec coherency to get it into alt/az.

        Parameters
        ----------
        telescope_location : astropy EarthLocation object
            Location of the telescope.

        Returns
        -------
        array of floats
            Rotation matrix that takes the coherency from (RA,Dec) --> (Alt,Az),
            shape (2, 2, Ncomponents).
        """
        basis_rotation_matrix = self._calc_rotation_matrix(telescope_location)

        # Find mathematical points and vectors for RA/Dec
        theta_radec = np.pi / 2. - self.dec.rad
        phi_radec = self.ra.rad

        # Find mathematical points and vectors for Alt/Az
        theta_altaz = np.pi / 2. - self.alt_az[0, :]
        phi_altaz = self.alt_az[1, :]

        coherency_rot_matrix = np.zeros((2, 2, self.Ncomponents), dtype=np.float)
        for src_i in range(self.Ncomponents):
            coherency_rot_matrix[:, :, src_i] = scbt.spherical_basis_vector_rotation_matrix(
                theta_radec[src_i], phi_radec[src_i],
                basis_rotation_matrix[:, :, src_i],
                theta_altaz[src_i], phi_altaz[src_i])

        return coherency_rot_matrix

    def coherency_calc(self, telescope_location):
        """
        Calculate the local coherency in alt/az basis for this source at a time & location.

        The coherency is a 2x2 matrix giving electric field correlation in Jy.
        It's specified on the object as a coherency in the ra/dec basis,
        but must be rotated into local alt/az.

        Parameters
        ----------
        telescope_location : astropy EarthLocation object
            location of the telescope.

        Returns
        -------
        array of float
            local coherency in alt/az basis, shape (2, 2, Ncomponents)
        """
        if not isinstance(telescope_location, EarthLocation):
            raise ValueError('telescope_location must be an astropy EarthLocation object. '
                             'value was: {al}'.format(al=telescope_location))

        Ionly_mask = np.sum(self.stokes[1:, :, :], axis=0) == 0.0
        NstokesI = np.sum(Ionly_mask[0, :])   # Number of unpolarized sources

        # For unpolarized sources, there's no need to rotate the coherency matrix.
        coherency_local = self.coherency_radec.copy()
        if NstokesI < self.Ncomponents:
            # If there are any polarized sources, do rotation.
            rotation_matrix = self._calc_coherency_rotation(telescope_location)

            polarized_sources = np.where(~Ionly_mask)[0]

            # shape (2, 2, Ncomponents)
            rotation_matrix = rotation_matrix[..., polarized_sources]

            rotation_matrix_T = np.swapaxes(rotation_matrix, 0, 1)
            coherency_local[:, :, :, polarized_sources] = np.einsum(
                'aby,bcxy,cdy->adxy', rotation_matrix_T,
                self.coherency_radec[:, :, :, polarized_sources],
                rotation_matrix
            )

        # Zero coherency on sources below horizon.
        coherency_local[:, :, :, self.horizon_mask] *= 0.0

        return coherency_local

    def update_positions(self, time, telescope_location):
        """
        Calculate the altitude/azimuth positions for these sources
        From alt/az, calculate direction cosines (lmn)

        Args:
            time: astropy Time object
            telescope_location: astropy EarthLocation object

        Sets:
            self.pos_lmn: (3, Ncomponents)
            self.alt_az: (2, Ncomponents)
            self.time: (1,) Time object
        """

        if not isinstance(time, Time):
            raise ValueError('time must be an astropy Time object. '
                             'value was: {t}'.format(t=time))

        if not isinstance(telescope_location, EarthLocation):
            raise ValueError('telescope_location must be an astropy EarthLocation object. '
                             'value was: {al}'.format(al=telescope_location))

        if self.time == time:  # Don't repeat calculations
            return

        skycoord_use = SkyCoord(self.ra, self.dec, frame='icrs')
        source_altaz = skycoord_use.transform_to(AltAz(obstime=time,
                                                       location=telescope_location))

        time.location = telescope_location

        self.time = time
        alt_az = np.array([source_altaz.alt.rad, source_altaz.az.rad])

        self.alt_az = alt_az

        pos_l = np.sin(alt_az[1, :]) * np.cos(alt_az[0, :])
        pos_m = np.cos(alt_az[1, :]) * np.cos(alt_az[0, :])
        pos_n = np.sin(alt_az[0, :])

        self.pos_lmn[0, :] = pos_l
        self.pos_lmn[1, :] = pos_m
        self.pos_lmn[2, :] = pos_n

        # Horizon mask:
        self.horizon_mask = self.alt_az[0, :] < 0.0

    def __eq__(self, other):
        time_check = (self.time is None and other.time is None)
        if not time_check:
            time_check = np.isclose(self.time, other.time)
        return (np.allclose(self.ra.deg, other.ra.deg, atol=self.pos_tol)
                and np.allclose(self.stokes, other.stokes)
                and np.all(self.name == other.name)
                and time_check)

    def get_size(self):
        """
        Estimate the SkyModel memory footprint in bytes
        """
        return estimate_skymodel_memory_usage(self.Ncomponents, self.Nfreqs)


def read_healpix_hdf5(hdf5_filename):
    """
    Read hdf5 healpix files using h5py and get a healpix map, indices and frequencies

    Parameters
    ----------
    hdf5_filename : path and name of the hdf5 file to read

    Returns
    -------
    hpmap : array_like of float
        Stokes-I surface brightness in K, for a set of pixels
        Shape (Ncomponents, Nfreqs)
    indices : array_like, int
        Corresponding HEALPix indices for hpmap.
    freqs : array_like, float
        Frequencies in Hz. Shape (Nfreqs)
    """
    f = h5py.File(hdf5_filename, 'r')
    hpmap = f['data'][0, ...]    # Remove Nskies axis.
    indices = f['indices'][()]
    freqs = f['freqs'][()]
    return hpmap, indices, freqs


def healpix_to_sky(hpmap, indices, freqs):
    """
    Convert a healpix map in K to a set of point source components in Jy.

    Parameters
    ----------
    hpmap : array_like of float
        Stokes-I surface brightness in K, for a set of pixels
        Shape (Ncomponents, Nfreqs)
    indices : array_like, int
        Corresponding HEALPix indices for hpmap.
    freqs : array_like, float
        Frequencies in Hz. Shape (Nfreqs)

    Returns
    -------
    SkyModel

    Notes
    -----
    Currently, this function only converts a HEALPix map with a frequency axis.
    """
    Nside = astropy_healpix.npix_to_nside(hpmap.shape[-1])
    ra, dec = astropy_healpix.healpix_to_lonlat(indices, Nside)
    stokes = np.zeros((4, len(freqs), len(indices)))
    stokes[0] = (hpmap.T / simutils.jy2Tsr(freqs,
                 bm=astropy_healpix.nside_to_pixel_area(Nside).value, mK=False)
                 ).T
    sky = SkyModel(indices.astype('str'), ra, dec, stokes, freq_array=freqs, Nfreqs=len(freqs))
    return sky
