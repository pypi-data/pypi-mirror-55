# -*- mode: python; coding: utf-8 -*
# Copyright (c) 2018 Radio Astronomy Software Group
# Licensed under the 3-clause BSD License

from __future__ import absolute_import, division, print_function

import os
import sys
import time as pytime

import numpy as np
try:
    import psutil
    HAVE_PSUTIL = True
except ImportError:
    HAVE_PSUTIL = False
from astropy import _erfa as erfa
from astropy.coordinates import Angle
from astropy.coordinates.builtin_frames.utils import get_jd12
from astropy.time import Time
from astropy.constants import c
from six.moves import range

from . import version as simversion


def get_version_string():
    version_string = ('Simulated with pyuvsim version: ' + simversion.version + '.')
    if simversion.git_hash:
        version_string += ('  Git origin: ' + simversion.git_origin
                           + '.  Git hash: ' + simversion.git_hash
                           + '.  Git branch: ' + simversion.git_branch
                           + '.  Git description: ' + simversion.git_description + '.')
    return version_string


class progsteps:
    """
    Similar to a progress bar, this prints a percentage of task completion.

    Parameters
    ----------

    maxval : int
        Maximum value to count to.

    """

    def __init__(self, maxval=None):
        self.t0 = pytime.time()
        if maxval is None:
            raise ValueError("Maximum value is needed.")
        self.maxval = float(maxval)
        step = self.maxval * 0.01
        if step < 1.0:
            step = 1
        self.step = step
        self.curval = -1

    def update(self, count):
        """
        Update the progress bar.

        Parameters
        ----------
        count : int
            Current value of counter
        """
        if count >= self.curval + self.step:
            doprint = False
            if not self.curval == count:
                doprint = True
                self.curval = count
            if doprint:
                ostr = "{:0.2f}% completed. {:0.3f} minutes elapsed".format(
                    (count / self.maxval) * 100., (pytime.time() - self.t0) / 60.)
                ostr += '\n'
                print(ostr)
                sys.stdout.flush()

    def finish(self):
        self.update(self.maxval)


# The frame radio astronomers call the apparent or current epoch is the
# "true equator & equinox" frame, notated E_upsilon in the USNO circular
# astropy doesn't have this frame but it's pretty easy to adapt the CIRS frame
# by modifying the ra to reflect the difference between
# GAST (Grenwich Apparent Sidereal Time) and the earth rotation angle (theta)
def tee_to_cirs_ra(tee_ra, time):
    era = erfa.era00(*get_jd12(time, 'ut1'))
    theta_earth = Angle(era, unit='rad')

    assert (isinstance(time, Time))
    assert (isinstance(tee_ra, Angle))
    gast = time.sidereal_time('apparent', longitude=0)
    cirs_ra = tee_ra - (gast - theta_earth)
    return cirs_ra


def cirs_to_tee_ra(cirs_ra, time):
    era = erfa.era00(*get_jd12(time, 'ut1'))
    theta_earth = Angle(era, unit='rad')

    assert (isinstance(time, Time))
    assert (isinstance(cirs_ra, Angle))
    gast = time.sidereal_time('apparent', longitude=0)
    tee_ra = cirs_ra + (gast - theta_earth)
    return tee_ra


def altaz_to_zenithangle_azimuth(altitude, azimuth):
    """
    Convert from astropy altaz convention to UVBeam az/za convention.

    Args:
        altitude: in radians
        azimuth: in radians in astropy convention: East of North (N=0, E=pi/2)

    Returns:
        zenith_angle in radians
        azimuth in radians in uvbeam convention: North of East(East=0, North=pi/2)
    """
    input_alt = np.array(altitude)
    input_az = np.array(azimuth)
    if input_alt.size != input_az.size:
        raise ValueError('number of altitude and azimuth values must match.')

    zenith_angle = np.pi / 2 - input_alt
    new_azimuth = np.pi / 2 - input_az

    if new_azimuth.size > 1:
        wh_neg = np.where(new_azimuth < -1e-9)
        if wh_neg[0].size > 0:
            new_azimuth[wh_neg] = new_azimuth[wh_neg] + np.pi * 2
    else:
        if new_azimuth < -1e-9:
            new_azimuth = new_azimuth + np.pi * 2

    return zenith_angle, new_azimuth


def zenithangle_azimuth_to_altaz(zenith_angle, azimuth):
    """
    Convert from astropy altaz convention to UVBeam az/za convention.

    Args:
        zenith_angle: in radians
        azimuth: in radians in uvbeam convention: North of East(East=0, North=pi/2)

    Returns:
        altitude in radians
        azimuth in radians in astropy convention: East of North (N=0, E=pi/2)
    """
    input_za = np.array(zenith_angle)
    input_az = np.array(azimuth)
    if input_za.size != input_az.size:
        raise ValueError('number of zenith_angle and azimuth values must match.')

    altitude = np.pi / 2 - input_za
    new_azimuth = np.pi / 2 - input_az

    if new_azimuth.size > 1:
        wh_neg = np.where(new_azimuth < -1e-9)
        if wh_neg[0].size > -1e-9:
            new_azimuth[wh_neg] = new_azimuth[wh_neg] + np.pi * 2
    else:
        if new_azimuth < -1e-9:
            new_azimuth = new_azimuth + np.pi * 2

    return altitude, new_azimuth


def strip_extension(filepath, ext=None):
    """ Remove extension from file. """
    if '.' not in filepath:
        return filepath, ''
    file_list = filepath.split('.')
    if ext is not None:
        return filepath[:-len(ext) - 1], '.' + ext
    ext = file_list[-1]
    # miriad files might not have an extension
    # limited list of recognized extensions
    if ext not in ['uvfits', 'uvh5', 'yaml']:
        return filepath, ''
    return ".".join(file_list[:-1]), '.' + file_list[-1]


def check_file_exists_and_increment(filepath, extension=None):
    """
        Given filepath (path + filename), check if it exists. If so, add a _1
        at the end, if that exists add a _2, and so on.
    """
    base_filepath, ext = strip_extension(filepath, extension)
    bf_list = base_filepath.split('_')
    if bf_list[-1].isdigit():
        base_filepath = '_'.join(bf_list[:-1])
    n = 0
    while os.path.exists(filepath):
        filepath = "{}_{}".format(base_filepath, n) + ext
        n += 1
    return filepath


def write_uvdata(uv_obj, param_dict, return_filename=False, dryrun=False, out_format=None):
    """
    Parse output file information from parameters and write uvfits to file.

    Args:
        uv_obj: UVData object to write out.
        param_dict: parameter dictionary defining output path, filename, and
                    whether or not to clobber.
        return_filename: (Default false) Return the file path
        dryrun: (Default false) Don't write to file.
        out_format: (Default uvfits) Write as uvfits/miriad/uvh5

    Returns:
        File path, if return_filename is True
    """
    if 'filing' in param_dict.keys():
        param_dict = param_dict['filing']
    if 'outdir' not in param_dict:
        param_dict['outdir'] = '.'
    if 'output_format' in param_dict:
        out_format = param_dict['output_format']
    elif out_format is None:
        out_format = 'uvfits'

    if 'outfile_name' not in param_dict or param_dict['outfile_name'] == '':
        outfile_prefix = ""
        outfile_suffix = "results"
        if 'outfile_prefix' in param_dict:
            outfile_prefix = param_dict['outfile_prefix']
        if 'outfile_suffix' in param_dict:
            outfile_suffix = param_dict['outfile_suffix']
        outfile_name = "_".join([outfile_prefix, outfile_suffix])
        outfile_name = os.path.join(param_dict['outdir'], outfile_name)
    else:
        outfile_name = os.path.join(param_dict['outdir'], param_dict['outfile_name'])

    if not os.path.exists(param_dict['outdir']):
        os.makedirs(param_dict['outdir'])

    if out_format == 'uvfits':
        if not outfile_name.endswith(".uvfits"):
            outfile_name = outfile_name + ".uvfits"

    if out_format == 'uvh5':
        if not outfile_name.endswith(".uvh5"):
            outfile_name = outfile_name + ".uvh5"

    noclobber = ('clobber' not in param_dict) or not bool(param_dict['clobber'])
    if noclobber:
        outfile_name = check_file_exists_and_increment(outfile_name)

    print('Outfile path: ', outfile_name)
    if not dryrun:
        if out_format == 'uvfits':
            uv_obj.write_uvfits(outfile_name, force_phase=True, spoof_nonessential=True)
        elif out_format == 'miriad':
            uv_obj.write_miriad(outfile_name, clobber=not noclobber)
        elif out_format == 'uvh5':
            uv_obj.write_uvh5(outfile_name)
        else:
            raise ValueError(
                "Invalid output format. Options are \" uvfits\", \"uvh5\", or \"miriad\"")
    if return_filename:
        return outfile_name


def get_avail_memory():
    """
    Method for estimating the virtual memory available (in bytes)
    on the current node to a running process.

    Currently only supports the SLURM array scheduler.

    If this is not called from within a SLURM task, it will estimate
    using psutils methods.
    """
    if not HAVE_PSUTIL:
        raise ImportError("You need psutils to estimate available memory. "
                          "Install it by running pip install pyuvsim[sim] "
                          "or pip install pyuvsim[all] if you also want "
                          "h5py and line_profiler installed.")

    slurm_key = 'SLURM_MEM_PER_NODE'
    if slurm_key in os.environ:
        return float(os.environ[slurm_key]) * 1e6  # MB -> B

    return psutil.virtual_memory().available


def iter_array_split(part_index, N, M):
    """
    Returns an iterator giving the indices of `part` below:
        part = np.array_split(np.arange(N), M)[part_index]

    This mimics the behavior of array_split without having to make
    the whole array that will be split.
    """

    Neach_section, extras = divmod(N, M)
    if part_index < extras:
        length = Neach_section + 1
        start = part_index * (length)
        end = start + length
    else:
        length = Neach_section
        start = extras * (Neach_section + 1) + (part_index - extras) * length
        end = start + length

    return range(start, end), end - start


def stokes_to_coherency(stokes_vector):
    """
    Convert Stokes vector to coherency matrix

    Parameters
    ----------
    stokes_vector : array_like of float
        Vector(s) of stokes parameters in order [I, Q, U, V], shape(4,) or (4, Nfreqs, Ncomponents)

    Returns
    -------
    coherency matrix : array of float
        Array of coherencies, shape (2, 2) or (2, 2, Ncomponents)
    """
    stokes_arr = np.atleast_1d(np.asarray(stokes_vector))
    initial_shape = stokes_arr.shape
    if initial_shape[0] != 4:
        raise ValueError('First dimension of stokes_vector must be length 4.')

    if stokes_arr.size == 4 and len(initial_shape) == 1:
        stokes_arr = stokes_arr[:, np.newaxis, np.newaxis]

    coherency = .5 * np.array([[stokes_arr[0, :, :] + stokes_arr[1, :, :],
                                stokes_arr[2, :, :] - 1j * stokes_arr[3, :, :]],
                               [stokes_arr[2, :, :] + 1j * stokes_arr[3, :, :],
                                stokes_arr[0, :, :] - stokes_arr[1, :, :]]])

    if stokes_arr.size == 4 and len(initial_shape) == 1:
        coherency = np.squeeze(coherency)
    return coherency


def coherency_to_stokes(coherency_matrix):
    """
    Convert coherency matrix to vector of 4 Stokes parameter in order [I, Q, U, V]

    Parameters
    ----------
    coherency matrix : array_like of float
        Array of coherencies, shape (2, 2) or (2, 2, Ncomponents)

    Returns
    -------
    stokes_vector : array of float
        Vector(s) of stokes parameters, shape(4,) or (4, Ncomponents)
    """
    coherency_arr = np.asarray(coherency_matrix)
    initial_shape = coherency_arr.shape
    if len(initial_shape) < 2 or initial_shape[0] != 2 or initial_shape[1] != 2:
        raise ValueError('First two dimensions of coherency_matrix must be length 2.')

    if coherency_arr.size == 4 and len(initial_shape) == 2:
        coherency_arr = coherency_arr[:, :, np.newaxis]

    stokes = np.array([coherency_arr[0, 0, :] + coherency_arr[1, 1, :],
                       coherency_arr[0, 0, :] - coherency_arr[1, 1, :],
                       coherency_arr[0, 1, :] + coherency_arr[1, 0, :],
                       -(coherency_arr[0, 1, :] - coherency_arr[1, 0, :]).imag]).real
    if coherency_arr.size == 4 and len(initial_shape) == 2:
        stokes = np.squeeze(stokes)

    return stokes


def jy2Tsr(f, bm=1.0, mK=False):
    '''Return [K sr] / [Jy] vs. frequency (in Hz)
        Arguments:
            f = frequencies (Hz)
            bm = Reference solid angle in steradians (Defaults to 1)
            mK = Return in mK sr instead of K sr
    '''
    c_cmps = c.to('cm/s').value  # cm/s
    k_boltz = 1.380658e-16   # erg/K
    lam = c_cmps / f  # cm
    fac = 1.0
    if mK:
        fac = 1e3
    return 1e-23 * lam**2 / (2 * k_boltz * bm) * fac
