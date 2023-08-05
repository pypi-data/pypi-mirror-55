"""
This file contains several helper functions to calculate spectral power from
1D and 2D EEG data.
"""
import mne
import numpy as np
import pandas as pd
from scipy import signal
from scipy.integrate import simps
from scipy.interpolate import RectBivariateSpline


__all__ = ['bandpower', 'bandpower_from_psd', 'irasa', 'stft_power']


def bandpower(data, sf=None, ch_names=None, hypno=None, include=(2, 3),
              win_sec=4, relative=True,
              bands=[(0.5, 4, 'Delta'), (4, 8, 'Theta'), (8, 12, 'Alpha'),
                     (12, 30, 'Beta'), (30, 40, 'Gamma')],
              kwargs_welch=dict(average='median', window='hamming')):
    """
    Calculate the Welch bandpower for each channel and, if specified,
    for each sleep stage.

    .. versionadded:: 0.1.6

    Parameters
    ----------
    data : np.array_like or :py:class:`mne.io.BaseRaw`
        1D or 2D EEG data. Can also be a :py:class:`mne.io.BaseRaw`, in which
        case ``data``, ``sf``, and ``ch_names`` will be automatically
        extracted, and ``data`` will also be converted from Volts (MNE default)
        to micro-Volts (YASA).
    sf : float
        The sampling frequency of data AND the hypnogram.
        Can be omitted if ``data`` is a :py:class:`mne.io.BaseRaw`.
    ch_names : list
        List of channel names, e.g. ['Cz', 'F3', 'F4', ...]. If None,
        channels will be labelled ['CHAN001', 'CHAN002', ...].
        Can be omitted if ``data`` is a :py:class:`mne.io.BaseRaw`.
    hypno : array_like
        Sleep stage vector (hypnogram). If the hypnogram is loaded, the
        bandpower will be extracted for each sleep stage defined in
        ``include``.

        The hypnogram must have the exact same number of samples as ``data``.
        To upsample your hypnogram, please refer to
        :py:func:`yasa.hypno_upsample_to_data`.

        .. note::
            The default hypnogram format in YASA is a 1D integer
            vector where:

            - -1 = Artefact / Movement
            - 0 = Wake
            - 1 = N1 sleep
            - 2 = N2 sleep
            - 3 = N3 sleep
            - 4 = REM
    include : tuple, list or int
        Values in ``hypno`` that will be included in the mask. The default is
        (2, 3), meaning that the bandpower are sequentially calculated
        for N2 and N3 sleep. This has no effect when ``hypno`` is None.
    win_sec : int or float
        The length of the sliding window, in seconds, used for the Welch PSD
        calculation. Ideally, this should be at least two times the inverse of
        the lower frequency of interest (e.g. for a lower frequency of interest
        of 0.5 Hz, the window length should be at least 2 * 1 / 0.5 =
        4 seconds).
    relative : boolean
        If True, bandpower is divided by the total power between the min and
        max frequencies defined in ``band``.
    bands : list of tuples
        List of frequency bands of interests. Each tuple must contain the
        lower and upper frequencies, as well as the band name
        (e.g. (0.5, 4, 'Delta')).
    kwargs_welch : dict
        Optional keywords arguments that are passed to the
        :py:func:`scipy.signal.welch` function.

    Returns
    -------
    bandpowers : :py:class:`pandas.DataFrame`
        Bandpower dataframe, in which each row is a channel and each column
        a spectral band.

    Notes
    -----
    For an example of how to use this function, please refer to
    https://github.com/raphaelvallat/yasa/blob/master/notebooks/10_bandpower.ipynb
    """
    # Check if input data is a MNE Raw object
    if isinstance(data, mne.io.BaseRaw):
        sf = data.info['sfreq']  # Extract sampling frequency
        ch_names = data.ch_names  # Extract channel names
        data = data.get_data() * 1e6  # Convert from V to uV
        _, npts = data.shape
    else:
        # Safety checks
        assert isinstance(data, np.ndarray), 'Data must be a numpy array.'
        data = np.atleast_2d(data)
        assert data.ndim == 2, 'Data must be of shape (nchan, n_samples).'
        nchan, npts = data.shape
        assert nchan < npts, 'Data must be of shape (nchan, n_samples).'
        assert sf is not None, 'sf must be specified if passing a numpy array.'
        assert isinstance(sf, (int, float))
        if ch_names is None:
            ch_names = ['CHAN' + str(i + 1).zfill(3) for i in range(nchan)]
        else:
            ch_names = np.atleast_1d(np.asarray(ch_names, dtype=str))
            assert ch_names.ndim == 1, 'ch_names must be 1D.'
            assert len(ch_names) == nchan, 'ch_names must match data.shape[0].'

    win = int(win_sec * sf)  # nperseg

    if hypno is None:
        # Calculate the PSD over the whole data
        freqs, psd = signal.welch(data, sf, nperseg=win, **kwargs_welch)
        return bandpower_from_psd(psd, freqs, ch_names,
                                  bands=bands,
                                  relative=relative).set_index('Chan')
    else:
        # Per each sleep stage defined in ``include``.
        hypno = np.asarray(hypno)
        assert include is not None, 'include cannot be None if hypno is given'
        include = np.atleast_1d(np.asarray(include))
        assert hypno.ndim == 1, 'Hypno must be a 1D array.'
        assert hypno.size == npts, 'Hypno must have same size as data.shape[1]'
        assert include.size >= 1, '`include` must have at least one element.'
        assert hypno.dtype.kind == include.dtype.kind, ('hypno and include '
                                                        'must have same dtype')
        assert np.in1d(hypno, include).any(), ('None of the stages '
                                               'specified in `include` '
                                               'are present in hypno.')
        # Initialize empty dataframe and loop over stages
        df_bp = pd.DataFrame([])
        for stage in include:
            if stage not in hypno:
                continue
            data_stage = data[:, hypno == stage]
            freqs, psd = signal.welch(data_stage, sf, nperseg=win,
                                      **kwargs_welch)
            bp_stage = bandpower_from_psd(psd, freqs, ch_names, bands=bands,
                                          relative=relative)
            bp_stage['Stage'] = stage
            df_bp = df_bp.append(bp_stage)
        return df_bp.set_index(['Stage', 'Chan'])


def bandpower_from_psd(psd, freqs, ch_names=None, bands=[(0.5, 4, 'Delta'),
                       (4, 8, 'Theta'), (8, 12, 'Alpha'), (12, 30, 'Beta'),
                       (30, 40, 'Gamma')], relative=True):
    """Compute the average power of the EEG in specified frequency band(s)
    given a pre-computed PSD.

    .. versionadded:: 0.1.5

    Parameters
    ----------
    psd : array_like
        Power spectral density of data, in uV^2/Hz.
        Must be of shape (n_channels, n_freqs).
        See :py:func:`scipy.signal.welch` for more details.
    freqs : array_like
        Array of frequencies.
    ch_names : list
        List of channel names, e.g. ['Cz', 'F3', 'F4', ...]. If None,
        channels will be labelled ['CHAN001', 'CHAN002', ...].
    bands : list of tuples
        List of frequency bands of interests. Each tuple must contain the
        lower and upper frequencies, as well as the band name
        (e.g. (0.5, 4, 'Delta')).
    relative : boolean
        If True, bandpower is divided by the total power between the min and
        max frequencies defined in ``band`` (default 0.5 to 40 Hz).

    Returns
    -------
    bandpowers : :py:class:`pandas.DataFrame`
        Bandpower dataframe, in which each row is a channel and each column
        a spectral band.
    """
    # Safety checks
    freqs = np.asarray(freqs)
    assert freqs.ndim == 1
    psd = np.atleast_2d(psd)
    assert psd.ndim == 2, 'PSD must be of shape (n_channels, n_freqs).'
    all_freqs = np.hstack([[b[0], b[1]] for b in bands])
    fmin, fmax = min(all_freqs), max(all_freqs)
    idx_good_freq = np.logical_and(freqs >= fmin, freqs <= fmax)
    freqs = freqs[idx_good_freq]
    res = freqs[1] - freqs[0]
    nchan = psd.shape[0]
    assert nchan < psd.shape[1], 'PSD must be of shape (n_channels, n_freqs).'
    if ch_names is not None:
        ch_names = np.atleast_1d(np.asarray(ch_names, dtype=str))
        assert ch_names.ndim == 1, 'ch_names must be 1D.'
        assert len(ch_names) == nchan, 'ch_names must match psd.shape[0].'
    else:
        ch_names = ['CHAN' + str(i + 1).zfill(3) for i in range(nchan)]
    bp = np.zeros((nchan, len(bands)), dtype=np.float)
    psd = psd[:, idx_good_freq]
    total_power = simps(psd, dx=res)
    total_power = total_power[..., np.newaxis]

    # Enumerate over the frequency bands
    labels = []
    for i, band in enumerate(bands):
        b0, b1, la = band
        labels.append(la)
        idx_band = np.logical_and(freqs >= b0, freqs <= b1)
        bp[:, i] = simps(psd[:, idx_band], dx=res)

    if relative:
        bp /= total_power

    # Convert to DataFrame
    bp = pd.DataFrame(bp, columns=labels)
    bp['FreqRes'] = res
    # bp['WindowSec'] = 1 / res
    bp['Relative'] = relative
    bp['Chan'] = ch_names
    bp = bp.set_index('Chan').reset_index()
    # Add hidden attributes
    bp.bands_ = str(bands)
    return bp


def irasa(data, sf=None, ch_names=None, band=(1, 30),
          hset=np.arange(1.1, 1.95, 0.05), return_fit=True, win_sec=4,
          kwargs_welch=dict(average='median', window='hamming')):
    """
    Separate the aperiodic (= fractal, or 1/f) and oscillatory component of the
    power spectra of EEG data using the IRASA method.

    .. versionadded:: 0.1.7

    Parameters
    ----------
    data : :py:class:`numpy.ndarray` or :py:class:`mne.io.BaseRaw`
        1D or 2D EEG data. Can also be a :py:class:`mne.io.BaseRaw`, in which
        case ``data``, ``sf``, and ``ch_names`` will be automatically
        extracted, and ``data`` will also be converted from Volts (MNE default)
        to micro-Volts (YASA).
    sf : float
        The sampling frequency of data AND the hypnogram.
        Can be omitted if ``data`` is a :py:class:`mne.io.BaseRaw`.
    ch_names : list
        List of channel names, e.g. ['Cz', 'F3', 'F4', ...]. If None,
        channels will be labelled ['CHAN001', 'CHAN002', ...].
        Can be omitted if ``data`` is a :py:class:`mne.io.BaseRaw`.
    band : tuple or None
        Broad band frequency range.
        Default is 1 to 30 Hz.
    hset : :py:class:`numpy.ndarray`
        Resampling factors used in IRASA calculation. Default is to use a range
        of values from 1.1 to 1.9 with an increment of 0.05.
    return_fit : boolean
        If True (default), fit an exponential function to the aperiodic PSD
        and return the fit parameters (intercept, slope) and :math:`R^2` of
        the fit.

        The aperiodic signal, :math:`L`, is modeled using an exponential
        function in semilog-power space (linear frequencies and log PSD) as:

        .. math:: L = a + \\text{log}(F^b)

        where :math:`a` is the intercept, :math:`b` is the slope, and
        :math:`F` the vector of input frequencies.
    win_sec : int or float
        The length of the sliding window, in seconds, used for the Welch PSD
        calculation. Ideally, this should be at least two times the inverse of
        the lower frequency of interest (e.g. for a lower frequency of interest
        of 0.5 Hz, the window length should be at least 2 * 1 / 0.5 =
        4 seconds).
    kwargs_welch : dict
        Optional keywords arguments that are passed to the
        :py:func:`scipy.signal.welch` function.

    Returns
    -------
    freqs : :py:class:`numpy.ndarray`
        Frequency vector.
    psd_aperiodic : :py:class:`numpy.ndarray`
        The fractal (= aperiodic) component of the PSD.
    psd_oscillatory : :py:class:`numpy.ndarray`
        The oscillatory (= periodic) component of the PSD.
    fit_params : :py:class:`pandas.DataFrame` (optional)
        Dataframe of fit parameters. Only if ``return_fit=True``.

    Notes
    -----
    The Irregular-Resampling Auto-Spectral Analysis (IRASA) method is
    described in Wen & Liu (2016). In a nutshell, the goal is to separate the
    fractal and oscillatory components in the power spectrum of EEG signals.

    The steps are:

    1. Compute the original power spectral density (PSD) using Welch's method.
    2. Resample the EEG data by multiple non-integer factors and their
       reciprocals (:math:`h` and :math:`1/h`).
    3. For every pair of resampled signals, calculate the PSD and take the
       geometric mean of both. In the resulting PSD, the power associated with
       the oscillatory component is redistributed away from its original
       (fundamental and harmonic) frequencies by a frequency offset that varies
       with the resampling factor, whereas the power solely attributed to the
       fractal component remains the same power-law statistical distribution
       independent of the resampling factor.
    4. It follows that taking the median of the PSD of the variously
       resampled signals can extract the power spectrum of the fractal
       component, and the difference between the original power spectrum and
       the extracted fractal spectrum offers an approximate estimate of the
       power spectrum of the oscillatory component.

    Note that an estimate of the original PSD can be calculated by simply
    adding ``psd = psd_aperiodic + psd_oscillatory``.

    For an example of how to use this function, please refer to
    https://github.com/raphaelvallat/yasa/blob/master/notebooks/11_IRASA.ipynb

    References
    ----------
    .. [1] Wen, H., & Liu, Z. (2016). Separating Fractal and Oscillatory
           Components in the Power Spectrum of Neurophysiological Signal.
           Brain Topography, 29(1), 13–26.
           https://doi.org/10.1007/s10548-015-0448-0

    .. [2] https://github.com/fieldtrip/fieldtrip/blob/master/specest/

    .. [3] https://github.com/fooof-tools/fooof

    .. [4] https://www.biorxiv.org/content/10.1101/299859v1
    """
    import fractions
    # Check if input data is a MNE Raw object
    if isinstance(data, mne.io.BaseRaw):
        sf = data.info['sfreq']  # Extract sampling frequency
        ch_names = data.ch_names  # Extract channel names
        data = data.get_data() * 1e6  # Convert from V to uV
    else:
        # Safety checks
        assert isinstance(data, np.ndarray), 'Data must be a numpy array.'
        data = np.atleast_2d(data)
        assert data.ndim == 2, 'Data must be of shape (nchan, n_samples).'
        nchan, npts = data.shape
        assert nchan < npts, 'Data must be of shape (nchan, n_samples).'
        assert sf is not None, 'sf must be specified if passing a numpy array.'
        assert isinstance(sf, (int, float))
        if ch_names is None:
            ch_names = ['CHAN' + str(i + 1).zfill(3) for i in range(nchan)]
        else:
            ch_names = np.atleast_1d(np.asarray(ch_names, dtype=str))
            assert ch_names.ndim == 1, 'ch_names must be 1D.'
            assert len(ch_names) == nchan, 'ch_names must match data.shape[0].'

    # Check the other arguments
    hset = np.asarray(hset)
    assert hset.ndim == 1, 'hset must be 1D.'
    assert hset.size > 1, '2 or more resampling fators are required.'
    hset = np.round(hset, 4)  # avoid float precision error with np.arange.
    band = sorted(band)
    assert band[0] > 0, 'first element of band must be > 0.'
    assert band[1] < (sf / 2), 'second element of band must be < (sf / 2).'
    win = int(win_sec * sf)  # nperseg

    # Calculate the original PSD over the whole data
    freqs, psd = signal.welch(data, sf, nperseg=win, **kwargs_welch)

    # Start the IRASA procedure
    psds = np.zeros((len(hset), *psd.shape))

    for i, h in enumerate(hset):
        # Get the upsampling/downsampling (h, 1/h) factors as integer
        rat = fractions.Fraction(str(h))
        up, down = rat.numerator, rat.denominator
        # Much faster than FFT-based resampling
        data_up = signal.resample_poly(data, up, down, axis=-1)
        data_down = signal.resample_poly(data, down, up, axis=-1)
        # Calculate the PSD using same params as original
        freqs_up, psd_up = signal.welch(data_up, h * sf, nperseg=win,
                                        **kwargs_welch)
        freqs_dw, psd_dw = signal.welch(data_down, sf / h, nperseg=win,
                                        **kwargs_welch)
        # Geometric mean of h and 1/h
        psds[i, :] = np.sqrt(psd_up * psd_dw)

    # Now we take the median PSD of all the resampling factors, which gives
    # a good estimate of the aperiodic component of the PSD.
    psd_aperiodic = np.median(psds, axis=0)

    # We can now calculate the oscillations (= periodic) component.
    psd_osc = psd - psd_aperiodic

    # Let's crop to the frequencies defined in band
    mask_freqs = np.ma.masked_outside(freqs, *band).mask
    freqs = freqs[~mask_freqs]
    psd_aperiodic = np.compress(~mask_freqs, psd_aperiodic, axis=-1)
    psd_osc = np.compress(~mask_freqs, psd_osc, axis=-1)

    if return_fit:
        # Aperiodic fit in semilog space for each channel
        from scipy.optimize import curve_fit
        intercepts, slopes, r_squared = [], [], []

        def func(t, a, b):
            # See https://github.com/fooof-tools/fooof
            return a + np.log(t**b)

        for y in np.atleast_2d(psd_aperiodic):
            y_log = np.log(y)
            # Note that here we define bounds for the slope but not for the
            # intercept.
            popt, pcov = curve_fit(func, freqs, y_log, p0=(2, -1),
                                   bounds=((-np.inf, -10), (np.inf, 2)))
            intercepts.append(popt[0])
            slopes.append(popt[1])
            # Calculate R^2: https://stackoverflow.com/q/19189362/10581531
            residuals = y_log - func(freqs, *popt)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y_log - np.mean(y_log))**2)
            r_squared.append(1 - (ss_res / ss_tot))

        # Create fit parameters dataframe
        fit_params = {'Chan': ch_names, 'Intercept': intercepts,
                      'Slope': slopes, 'R^2': r_squared,
                      'std(osc)': np.std(psd_osc, axis=-1, ddof=1)}
        return freqs, psd_aperiodic, psd_osc, pd.DataFrame(fit_params)
    else:
        return freqs, psd_aperiodic, psd_osc


def stft_power(data, sf, window=2, step=.2, band=(1, 30), interp=True,
               norm=False):
    """Compute the pointwise power via STFT and interpolation.

    Parameters
    ----------
    data : array_like
        Single-channel data.
    sf : float
        Sampling frequency of the data.
    window : int
        Window size in seconds for STFT.
        2 or 4 seconds are usually a good default.
        Higher values = higher frequency resolution = lower time resolution.
    step : int
        Step in seconds for the STFT.
        A step of 0.2 second (200 ms) is usually a good default.

        * If ``step`` == 0, overlap at every sample (slowest)
        * If ``step`` == nperseg, no overlap (fastest)

        Higher values = higher precision = slower computation.
    band : tuple or None
        Broad band frequency range.
        Default is 1 to 30 Hz.
    interp : boolean
        If True, a cubic interpolation is performed to ensure that the output
        is the same size as the input (= pointwise power).
    norm : bool
        If True, return bandwise normalized band power, i.e. for each time
        point, the sum of power in all the frequency bins equals 1.

    Returns
    -------
    f : :py:class:`numpy.ndarray`
        Frequency vector
    t : :py:class:`numpy.ndarray`
        Time vector
    Sxx : :py:class:`numpy.ndarray`
        Power in the specified frequency bins of shape (f, t)

    Notes
    -----
    2D Interpolation is done using
    :py:class:`scipy.interpolate.RectBivariateSpline`
    which is much faster than :py:class:`scipy.interpolate.interp2d`
    for a rectangular grid. The default is to use a bivariate spline with
    3 degrees.
    """
    # Safety check
    data = np.asarray(data)
    assert step <= window

    step = 1 / sf if step == 0 else step

    # Define STFT parameters
    nperseg = int(window * sf)
    noverlap = int(nperseg - (step * sf))

    # Compute STFT and remove the last epoch
    f, t, Sxx = signal.stft(data, sf, nperseg=nperseg, noverlap=noverlap,
                            detrend=False, padded=True)

    # Let's keep only the frequency of interest
    if band is not None:
        idx_band = np.logical_and(f >= band[0], f <= band[1])
        f = f[idx_band]
        Sxx = Sxx[idx_band, :]

    # Compute power
    Sxx = np.square(np.abs(Sxx))

    # Interpolate
    if interp:
        func = RectBivariateSpline(f, t, Sxx)
        t = np.arange(data.size) / sf
        Sxx = func(f, t)

    if norm:
        sum_pow = Sxx.sum(0).reshape(1, -1)
        np.divide(Sxx, sum_pow, out=Sxx)
    return f, t, Sxx
