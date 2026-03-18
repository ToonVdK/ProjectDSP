import numpy as np
from scipy.signal import butter, filtfilt

def apply_bandpass_filter(signal_data, lowcut, highcut, fs, order=4):
    """
    Applies a zero-phase Butterworth bandpass filter. If the filter shifts the ECG's R-peak by a different
    amount of time than the PPG's systolic peak, the PAT calculation will be inherently flawed.
    scipy.signal.filtfilt applies the filter forward then backward, resulting in exactly zero phase shift.
    """
    # Calculate the Nyquist frequency
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist

    # Design the Butterworth filter
    b, a = butter(order, [low, high], btype='band')

    # Apply the filter forwards and backwards (zero-phase).
    filtered_signal = filtfilt(b, a, signal_data)

    return filtered_signal

def normalize_zscore(signal_data):
    """
    Applies Z-score normalization so the signal has mean=0 and std=1. As outlined in the Treebupachatsakul paper,
    after filtering out the noise, you need to normalize the amplitude of the ECG and PPG signals using a z-score
    transformation. This step ensures the pipeline is robust against amplitude fluctuations caused by how tightly the
    sensor was attached to the patient
    """

    # Calculate the mean and standard deviation of the signal
    mean_val = np.mean(signal_data)
    std_val = np.std(signal_data)

    # Prevent division by zero just in case of a flatline signal
    if std_val == 0:
        return signal_data - mean_val

    # Normalize according to the formula z = (x-µ)/σ
    normalized_signal = (signal_data - mean_val) / std_val
    return normalized_signal

def preprocess_segment(ecg_segment, ppg_segment, fs=125):
    """
    Takes a raw ECG and PPG segment, filters them, and normalizes them.
    The sampling rate (fs) is 125 Hz based on the dataset specifications.
    """
    # ----- Bandpass Filtering -----
    # ECG: typically 0.5 Hz to 40 Hz to remove baseline wander and high-freq noise
    filtered_ecg = apply_bandpass_filter(ecg_segment, lowcut=0.5, highcut=40.0, fs=fs)

    # PPG: typically 0.5 Hz to 8 Hz (the pulse wave is a much lower frequency signal)
    filtered_ppg = apply_bandpass_filter(ppg_segment, lowcut=0.5, highcut=8.0, fs=fs)

    # ----- Z-Score Normalization -----
    clean_ecg = normalize_zscore(filtered_ecg)
    clean_ppg = normalize_zscore(filtered_ppg)

    return clean_ecg, clean_ppg
