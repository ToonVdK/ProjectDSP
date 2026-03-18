import numpy as np
from scipy.signal import find_peaks

def get_peaks(signal_data, fs=125):
    """
    Finds the peaks in a physiological signal.
    """
    # A normal resting heart rate is between 60-100 BPM.
    # That means peaks should be at least 0.6 seconds apart (100 BPM).
    # We set a minimum distance between peaks to avoid double-counting noise.
    min_distance_samples = int(0.3 * fs)

    # find_peaks returns the indices (sample numbers) of the peaks
    # We use prominence to ensure we only grab distinct peaks, ignoring tiny bumps
    peaks, _ = find_peaks(signal_data, distance=min_distance_samples, prominence=0.5)

    return peaks

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
