# -*- coding:utf-8 -*-
# Copyright (c) 2017, Combine Control Systems AB
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Combine Control Systems AB nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.
# IN NO EVENT SHALL COMBINE CONTROL SYSTEMS AB BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import inspect
import warnings

import numpy as np


def _find_peaks(signal):
    """
    This function does not deal well with NaN values, so make sure to remove
    them before calling.
    """
    import scipy.signal

    # Pass plateau_size as tuple of None to get left_/right_edges returned but
    # still get all peaks.
    _, peaks_dict = scipy.signal.find_peaks(signal, plateau_size=(None, None))

    res = np.zeros_like(signal, dtype=bool)
    for left, right in zip(peaks_dict['left_edges'],
                           peaks_dict['right_edges']):
        res[left:right+1] = True
    return res


def _get_parts(signal):
    """
    Return a generator over non-masked, non-NaN parts of signal.
    Each part is returned as a tuple with the signal part and a boolean saying
    if the part consist of NaN+masked values (True) or not (False).
    """
    if signal.dtype.kind == 'f':
        mask = np.isnan(signal)
    else:
        mask = None
    if isinstance(signal, np.ma.MaskedArray):
        if mask is None:
            mask = signal.mask
        else:
            mask = mask.filled(True)

    if mask is None:
        signal_parts = [signal]
        masked_parts = [False]
    else:
        splits = np.flatnonzero(np.logical_xor(mask[1:], mask[:-1])) + 1
        signal_parts = np.split(signal, splits)
        masked_parts = [np.any(part) for part in np.split(mask, splits)]

    return zip(signal_parts, masked_parts)


class EventDetection(object):
    """Container class for event detection functions."""

    @staticmethod
    def changed(signal):
        """Return a boolean array which is True at each position where signal
        is different than at the previous position. The first element in the
        returned array is always False.

        Parameters
        ----------
        signal : np.array
            The array the function should be performed on.

        Returns
        -------
        np.array
            An array of booleans with the same length as signal.
        """
        if not signal.size:
            return np.array([], dtype=bool)

        if signal.dtype.kind == 'f':
            isnan = np.isnan(signal)
            nans = np.logical_or(isnan[:-1], isnan[1:])
        else:
            nans = np.zeros((signal.size - 1,), dtype=bool)

        diff = np.logical_and(signal[:-1] != signal[1:], np.logical_not(nans))
        if np.ma.isMaskedArray(diff):
            diff = np.ma.concatenate(([False], diff))
            if np.ma.getmaskarray(signal)[0]:
                diff.mask = np.ma.getmaskarray(diff)
                diff.mask[0] = True
            return diff
        else:
            return np.concatenate(([False], diff))

    @staticmethod
    def changed_up(signal):
        """Return a boolean array which is True at each position where signal
        is greater than at the previous position. The first element in the
        returned array is always False.

        Parameters
        ----------
        signal : np.array
            The array the function should be performed on.

        Returns
        -------
        np.array
            An array of booleans with the same length as signal.
        """
        if not signal.size:
            return np.array([], dtype=bool)
        if signal.dtype.kind in 'bu':
            signal = signal.astype(int)

        if signal.dtype.kind == 'M':
            # Create timedelta dtype with same precision
            diff_dtype = (signal[:0] - signal[:0]).dtype
            zero = np.zeros((), dtype=diff_dtype)
        elif signal.dtype.kind == 'm':
            zero = np.zeros((), dtype=signal.dtype)
        else:
            zero = 0

        # Greater than ufunc prints a warning if there are NaNs in signal, but
        # we have a well defined behavior for NaNs, so no need for a warning.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            diff = np.diff(signal) > zero

        if np.ma.isMaskedArray(diff):
            diff = np.ma.concatenate(([False], diff))
            if np.ma.getmaskarray(signal)[0]:
                diff.mask = np.ma.getmaskarray(diff)
                diff.mask[0] = True
            return diff
        else:
            return np.concatenate(([False], diff))

    @staticmethod
    def changed_down(signal):
        """Return a boolean array which is True where ``signal`` is less than at
        the previous position. The first element in the returned array is
        always ``False``.

        Parameters
        ----------
        signal : np.array
            The array the function should be performed on.

        Returns
        -------
        np.array
            An index array with booleans with the same length as in_arr.
        """
        if not signal.size:
            return np.array([], dtype=bool)
        if signal.dtype.kind in 'bu':
            signal = signal.astype(int)

        if signal.dtype.kind == 'M':
            # Create timedelta dtype with same precision
            diff_dtype = (signal[:0] - signal[:0]).dtype
            zero = np.zeros((), dtype=diff_dtype)
        elif signal.dtype.kind == 'm':
            zero = np.zeros((), dtype=signal.dtype)
        else:
            zero = 0

        # Less than ufunc prints a warning if there are NaNs in signal, but we
        # have a well defined behavior for NaNs, so no need for a warning.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            diff = np.diff(signal) < zero

        if np.ma.isMaskedArray(diff):
            diff = np.ma.concatenate(([False], diff))
            if np.ma.getmaskarray(signal)[0]:
                diff.mask = np.ma.getmaskarray(diff)
                diff.mask[0] = True
            return diff
        else:
            return np.concatenate(([False], diff))

    @staticmethod
    def local_max(signal):
        """Return a boolean array which is True at each local maximum in
        signal, i.e. between an increase and a decrease in signal. Maxima at
        signal boundaries or near NaN aren't included.

        Parameters
        ----------
        signal : np.array
            The signal the function should be performed on.

        Returns
        -------
        np.array
            An array of booleans with the same length as signal.

        Examples
        --------
        >>> signal = np.array([1, 0, 1, 0, 1, 1, 2, 0])
        >>> peaks = np.array(
        ...     [False, False, True, False, False, False, True, False])
        >>> np.all(local_max(signal) == peaks)
        True
        """
        results = []
        for part, masked in _get_parts(signal):
            if masked:
                results.append(np.zeros(len(part), dtype=bool))
            else:
                results.append(_find_peaks(part))
        return np.concatenate(results)

    @staticmethod
    def local_min(signal):
        """Return a boolean array which is True at each local minimum in
        signal, i.e. between a decrease and an increase in signal. Minima at
        signal boundaries or near NaN aren't included.

        Parameters
        ----------
        signal : np.array
            The signal the function should be performed on.

        Returns
        -------
        np.array
            An array of booleans with the same length as signal.

        Examples
        --------
        >>> signal = np.array([1, 0, 1, 0, -1, -1, -2, 0])
        >>> peaks = np.array(
        ...     [False, True, False, False, False, False, True, False])
        >>> np.all(local_min(signal) == peaks)
        True
        """
        results = []
        for part, masked in _get_parts(signal):
            if masked:
                results.append(np.zeros(len(part), dtype=bool))
            else:
                if part.dtype.kind == 'u':
                    minus_part = -part.astype(int)
                elif part.dtype.kind == 'b':
                    minus_part = ~part
                elif part.dtype.kind == 'M':
                    minus_part = -part.astype(float)
                else:
                    minus_part = -part
                results.append(_find_peaks(minus_part))

        return np.concatenate(results)

    @staticmethod
    def global_max(signal):
        """Return a boolean array which is True when signal is at its maximum
        value.

        Parameters
        ----------
        signal : np.array
            The signal the function should be performed on.

        Returns
        -------
        np.array
            An array of booleans with the same length as signal.

        Examples
        --------
        >>> signal = np.array([1, 0, 1, 0, 1, 1, 2, 0])
        >>> max_ = np.array(
        ...     [False, False, False, False, False, False, True, False])
        >>> np.all(global_max(signal) == max_)
        True
        """
        if not signal.size:
            return np.array([], dtype=bool)

        if signal.dtype.kind == 'f':
            mask = signal == np.nanmax(signal)
        else:
            mask = signal == np.max(signal)
        if isinstance(mask, np.ma.MaskedArray):
            return mask.filled(False)
        else:
            return mask

    @staticmethod
    def global_min(signal):
        """Return a boolean array which is True when signal is at its minimum
        value.

        Parameters
        ----------
        signal : np.array
            The signal the function should be performed on.

        Returns
        -------
        np.array
            An array of booleans with the same length as signal.

        Examples
        --------
        >>> signal = np.array([1, 0, 1, 0, -1, -1, -2, 0])
        >>> min_ = np.array(
        ...     [False, False, False, False, False, False, True, False])
        >>> np.all(global_min(signal) == min_)
        True
        """
        if not signal.size:
            return np.array([], dtype=bool)

        if signal.dtype.kind == 'f':
            mask = signal == np.nanmin(signal)
        else:
            mask = signal == np.min(signal)
        if isinstance(mask, np.ma.MaskedArray):
            return mask.filled(False)
        else:
            return mask


GUI_DICT = {
    "Event detection": [
        ("Changed", "ca.changed(a)",
         inspect.getdoc(EventDetection.changed)),
        ("Changed up", "ca.changed_up(a)",
         inspect.getdoc(EventDetection.changed_up)),
        ("Changed down", "ca.changed_down(a)",
         inspect.getdoc(EventDetection.changed_down)),
        ("Local min", "ca.local_min(a)",
         inspect.getdoc(EventDetection.local_min)),
        ("Local max", "ca.local_max(a)",
         inspect.getdoc(EventDetection.local_max)),
        ("Global min", "ca.global_min(a)",
         "Return a boolean array which is True when signal is at its minimum "
         "value."),
        ("Global max", "ca.global_max(a)",
         "Return a boolean array which is True when signal is at its maximum "
         "value."),
    ]
}
