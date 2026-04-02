import numpy as np
from scipy.signal import find_peaks
from preprocess import preprocess_segment

def get_peaks(signal_data, fs=125):
    """
    Finds peaks in the PPG signal.
    """
    # A normal resting heart rate is between 60-100 BPM.
    # That means peaks should be at least 0.6 seconds apart (100 BPM).
    # We set a minimum distance between peaks to avoid double-counting noise.
    min_distance_samples = int(0.3 * fs)

    # find_peaks returns the indices (sample numbers) of the peaks
    # We use prominence to ensure we only grab distinct peaks, ignoring tiny bumps
    peaks, _ = find_peaks(signal_data, distance=min_distance_samples, prominence=0.5)

    return peaks


def pan_tompkins_r_peaks(ecg_signal, fs=125):
    """
    Implements a simplified Pan-Tompkins algorithm to find ECG R-peaks.
    """
    # Differentiation (Find the steep slopes)
    diff_ecg = np.diff(ecg_signal)
    diff_ecg = np.append(diff_ecg, 0)  # Keep array length the same

    #  Squaring (Exaggerate the steep slopes, suppress small waves)
    squared_ecg = diff_ecg ** 2

    # Moving Window Integration (Create a "lump" for each QRS complex)
    # A standard window is roughly 150ms
    window_width = int(0.15 * fs)
    integrated_ecg = np.convolve(squared_ecg, np.ones(window_width) / window_width, mode='same')

    # Find the "lumps" using the mean as an adaptive threshold
    threshold = np.mean(integrated_ecg)
    # Use find_peaks on the integrated signal (distance of 0.3s assumes max 200 BPM)
    qrs_lumps, _ = find_peaks(integrated_ecg, height=threshold, distance=int(0.3 * fs))

    # Map back to the original signal to find the exact R-peak
    r_peaks = []
    search_window = int(0.1 * fs)  # 100 ms search window around the lump

    for lump in qrs_lumps:
        start = max(0, lump - search_window)
        end = min(len(ecg_signal), lump + search_window)
        if start < end:
            # The actual R-peak is the local maximum in the original signal
            actual_r = start + np.argmax(ecg_signal[start:end])
            r_peaks.append(actual_r)

    # Return unique peaks in case windows slightly overlap
    return np.unique(r_peaks)


def get_p_peaks(ecg_signal, r_peaks, fs=125):
    """
    Finds the P-wave using a stricter physiological window to avoid T-waves.
    """
    p_peaks = []

    # A normal PR interval is 120ms to 200ms.
    # We restrict our search window to strictly 200ms to 40ms before the R-peak.
    # This prevents the window from accidentally swallowing the previous T-wave.
    search_start = int(0.20 * fs)  # 200ms before
    search_end = int(0.04 * fs)  # 40ms before

    for r_peak in r_peaks:
        start_idx = max(0, r_peak - search_start)
        end_idx = max(0, r_peak - search_end)

        if start_idx < end_idx:
            window_data = ecg_signal[start_idx:end_idx]
            p_peak_relative = np.argmax(window_data)
            p_peak_absolute = start_idx + p_peak_relative
            p_peaks.append(p_peak_absolute)

    return np.array(p_peaks)

def calculate_pat(ecg_peaks, ppg_peaks, fs=125):
    """
    Calculates the Pulse Arrival Time (PAT) for a segment.
    PAT is the time difference between an ECG R-peak and the *next* PPG peak.
    """
    pat_values = []

    # Go through each ECG peak
    for ecg_idx in ecg_peaks:
        # Find all PPG peaks that occur AFTER this ECG peak
        valid_ppg_peaks = ppg_peaks[ppg_peaks > ecg_idx]

        # If there is a subsequent PPG peak, calculate the time difference
        if len(valid_ppg_peaks) > 0:
            next_ppg_idx = valid_ppg_peaks[0]  # The very first one after the ECG peak

            # Difference in samples
            sample_diff = next_ppg_idx - ecg_idx

            # Convert samples to milliseconds (or seconds)
            time_diff_ms = (sample_diff / fs) * 1000

            # We filter out wildly wrong values (like a missed peak)
            if 0 < time_diff_ms < 1000:
                pat_values.append(time_diff_ms)

    # Return the average PAT for this 30-second segment
    if len(pat_values) > 0:
        return np.mean(pat_values)
    else:
        return np.nan  # Return Not-a-Number if no valid PATs were found


def calculate_ptt(p_peaks, ppg_peaks, fs=125):
    """
    Calculates PTT based on the time difference between the ECG P-peak and the next PPG peak.
    """
    ptt_values = []

    for p_idx in p_peaks:
        valid_ppg_peaks = ppg_peaks[ppg_peaks > p_idx]

        if len(valid_ppg_peaks) > 0:
            next_ppg_idx = valid_ppg_peaks[0]

            time_diff_ms = ((next_ppg_idx - p_idx) / fs) * 1000

            # PTT from the P-wave will be longer than PAT from the R-wave.
            if 0 < time_diff_ms < 1000:
                ptt_values.append(time_diff_ms)

    if len(ptt_values) > 0:
        return np.mean(ptt_values)
    else:
        return np.nan


def calculate_heart_rate(peaks, fs=125):
    """
    Calculates the average heart rate (in BPM) from a list of peak indices.
    """
    # We need at least 2 peaks to calculate the time between them
    if len(peaks) < 2:
        return np.nan

    # Calculate the distance between consecutive peaks in samples
    # np.diff subtracts each element from the next one (e.g., peak2 - peak1)
    intervals_samples = np.diff(peaks)

    # Convert those sample intervals into seconds
    intervals_seconds = intervals_samples / fs

    # Convert seconds into Beats Per Minute (BPM)
    instantaneous_bpm = 60.0 / intervals_seconds

    # Return the average BPM for this entire 30-second segment
    return np.mean(instantaneous_bpm)


def calculate_sqi(signal, peaks, fs=125):
    """
    Calculates a Signal Quality Index (SQI) between 0.0 (garbage) and 1.0 (perfect)
    based on Peak Regularity and Amplitude Stability.
    """
    if len(peaks) < 3:
        return 0.0  # Not enough peaks to evaluate

    # --- PEAK REGULARITY (Consistency of the intervals between beats) ---
    intervals = np.diff(peaks) / fs
    mean_interval = np.mean(intervals)
    std_interval = np.std(intervals)

    # Coefficient of Variation for intervals (CV = std / mean)
    cv_intervals = std_interval / mean_interval if mean_interval > 0 else 1.0

    # Map to a 0-1 score. A CV > 0.3 means massive arrhythmia or noise.
    regularity_score = max(0.0, 1.0 - (cv_intervals / 0.3))

    # --- AMPLITUDE STABILITY (Consistency of the peak heights) ---
    peak_amps = signal[peaks]
    mean_amp = np.mean(peak_amps)
    std_amp = np.std(peak_amps)

    # Coefficient of Variation for amplitudes
    cv_amps = std_amp / mean_amp if mean_amp > 0 else 1.0

    # Map to a 0-1 score. A CV > 0.5 means baseline wander is ruining the peaks.
    amplitude_score = max(0.0, 1.0 - (cv_amps / 0.5))

    # The final SQI is the average of both stability metrics
    return (regularity_score + amplitude_score) / 2.0


def fuse_heart_rates(ecg_hr, ppg_hr, ecg_sqi, ppg_sqi):
    """
    Calculates the weights and the fused Heart Rate based on the SQI scores.
    """
    # Prevent division by zero if both signals are completely corrupted
    total_sqi = ecg_sqi + ppg_sqi
    if total_sqi == 0:
        return np.nan, 0.0, 0.0

    # Calculate Weight Ratios
    w_ecg = ecg_sqi / total_sqi
    w_ppg = ppg_sqi / total_sqi

    # Fused HR Calculation
    hr_fused = (w_ecg * ecg_hr) + (w_ppg * ppg_hr)

    return hr_fused, w_ecg, w_ppg

def calculate_hrv(peaks, fs=125):
    """
    Calculates time-domain Heart Rate Variability (HRV) metrics: SDNN and RMSSD.
    Returns values in milliseconds.
    """
    if len(peaks) < 3:
        return np.nan, np.nan  # Need at least 3 peaks for successive differences

    # Calculate the time between peaks (RR intervals) in milliseconds
    rr_intervals_ms = np.diff(peaks) / fs * 1000.0

    # SDNN: Standard deviation of all RR intervals
    sdnn = np.std(rr_intervals_ms)

    # RMSSD: Root mean square of successive differences
    successive_diffs = np.diff(rr_intervals_ms)
    rmssd = np.sqrt(np.mean(successive_diffs**2))

    return sdnn, rmssd

def get_all_features(raw_ecg, raw_ppg, fs=125):
    """
    Master pipeline wrapper: Preprocesses, extracts peaks, and calculates all metrics.
    """
    # Preprocess the raw signals
    clean_ecg, clean_ppg = preprocess_segment(raw_ecg, raw_ppg, fs=fs)

    # Extract Peaks
    ecg_peaks = pan_tompkins_r_peaks(clean_ecg, fs=fs)
    ppg_peaks = get_peaks(clean_ppg, fs=fs)

    # Calculate Base Heart Rates
    ecg_hr = calculate_heart_rate(ecg_peaks, fs=fs)
    ppg_hr = calculate_heart_rate(ppg_peaks, fs=fs)

    # Calculate Signal Quality Indices (SQI)
    ecg_sqi = calculate_sqi(clean_ecg, ecg_peaks, fs=fs)
    ppg_sqi = calculate_sqi(clean_ppg, ppg_peaks, fs=fs)

    # Calculate Weights and Fused Heart Rate
    fused_hr, w_ecg, w_ppg = fuse_heart_rates(ecg_hr, ppg_hr, ecg_sqi, ppg_sqi)

    # Calculate Base HRV Metrics (SDNN & RMSSD)
    ecg_sdnn, ecg_rmssd = calculate_hrv(ecg_peaks, fs=fs)
    ppg_sdnn, ppg_rmssd = calculate_hrv(ppg_peaks, fs=fs)

    # Calculate Fused HRV Metrics
    fused_sdnn = (w_ecg * ecg_sdnn) + (w_ppg * ppg_sdnn)
    fused_rmssd = (w_ecg * ecg_rmssd) + (w_ppg * ppg_rmssd)

    # Package the metrics into a dictionary
    metrics = {
        'ecg_hr': ecg_hr,
        'ecg_sqi': ecg_sqi,
        'ecg_weight': w_ecg,
        'ppg_hr': ppg_hr,
        'ppg_sqi': ppg_sqi,
        'ppg_weight': w_ppg,
        'fused_hr': fused_hr,
        'fused_sdnn': fused_sdnn,
        'fused_rmssd': fused_rmssd
    }

    # Return the metrics AND the arrays needed for plotting
    return metrics, clean_ecg, clean_ppg, ecg_peaks, ppg_peaks