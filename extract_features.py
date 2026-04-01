import numpy as np
from scipy.signal import find_peaks

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
