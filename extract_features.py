import numpy as np
from scipy.signal import find_peaks

def get_peaks(signal_data, fs=125):
    """
    Finds the R-peaks in a physiological signal.
    """
    # A normal resting heart rate is between 60-100 BPM.
    # That means peaks should be at least 0.6 seconds apart (100 BPM).
    # We set a minimum distance between peaks to avoid double-counting noise.
    min_distance_samples = int(0.3 * fs)

    # find_peaks returns the indices (sample numbers) of the peaks
    # We use prominence to ensure we only grab distinct peaks, ignoring tiny bumps
    peaks, _ = find_peaks(signal_data, distance=min_distance_samples, prominence=0.5)

    return peaks


def get_p_peaks(ecg_signal, r_peaks, fs=125):
    """
    Finds the P-wave by searching backward from each established R-peak.
    """
    p_peaks = []

    # The P-wave typically occurs roughly 120ms to 250ms before the R-peak.
    # We define a search window looking backward from the R-peak.
    search_window_start = int(0.25 * fs)  # 250 ms before
    search_window_end = int(0.05 * fs)  # 50 ms before

    for r_peak in r_peaks:
        # Ensure we don't look past the beginning of the array
        start_idx = max(0, r_peak - search_window_start)
        end_idx = max(0, r_peak - search_window_end)

        if start_idx < end_idx:
            # Extract the window of data before the R-peak
            window_data = ecg_signal[start_idx:end_idx]

            # The P-peak is the local maximum in this window
            p_peak_relative = np.argmax(window_data)

            # Convert back to the absolute index in the main signal
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

            # A valid PAT is usually between 150ms and 300ms.
            # We filter out wildly wrong values (like a missed peak)
            if 100 < time_diff_ms < 400:
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
            # We widen the valid range to 100ms - 500ms.
            if 100 < time_diff_ms < 500:
                ptt_values.append(time_diff_ms)

    if len(ptt_values) > 0:
        return np.mean(ptt_values)
    else:
        return np.nan
