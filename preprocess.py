import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.signal import correlate, correlation_lags

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


def plot_pre_post_processing(raw_signal, clean_signal, fs=125, signal_name="ECG", zoom_sec=5.0):
    """
    Plots the raw signal and the processed signal side-by-side (stacked)
    for easy visual comparison.

    zoom_sec: How many seconds of data to show. 5 seconds is usually best
              to actually see the shape of the heartbeats.
    """
    # Create time axis in seconds
    N = len(raw_signal)
    t = np.arange(N) / fs

    # Create a mask to only plot the first 'zoom_sec' seconds
    # (Plotting all 30 seconds makes the waves too squished to see the noise reduction)
    mask = t < zoom_sec

    # Create a figure with 2 subplots (stacked vertically)
    # sharex=True makes sure zooming/panning affects both graphs equally
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

    # --- Top Graph: Raw Signal ---
    ax1.plot(t[mask], raw_signal[mask], color='gray', label=f'Raw Noisy {signal_name}')
    ax1.set_title(f'{signal_name} Preprocessing (First {zoom_sec}s)')
    ax1.set_ylabel('Amplitude (Raw)')
    ax1.legend(loc='upper right')
    ax1.grid(True)

    # --- Bottom Graph: Processed Signal ---
    # We use a different color to easily distinguish them
    color = 'blue' if signal_name.upper() == 'ECG' else 'green'
    ax2.plot(t[mask], clean_signal[mask], color=color, label=f'Filtered & Normalized {signal_name}')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Amplitude (Z-score)')
    ax2.legend(loc='upper right')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
