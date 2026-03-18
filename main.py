r"""
Example usage:
>  python main.py -d C:\Users\vande\PycharmProjects\DSP\ProjectBPAnalysis\data\ -p p000188 -i 1
"""
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

# Import the functions we built in the other files
from preprocess import preprocess_segment
from extract_features import get_peaks, get_p_peaks, calculate_pat, calculate_ptt


def load_signal(dbPath, patient, idx, signal_type):
    """Utility to load a specific raw signal segment."""
    file_path = os.path.join(dbPath, f"{patient}_{signal_type}.npy")
    wave = np.load(file_path)
    return wave[idx]


def main():
    parser = argparse.ArgumentParser(description='Run BP extraction pipeline with visual check.')
    parser.add_argument('-d', '--dbPath', help='path to .npy files', required=True)
    parser.add_argument('-p', '--patient', help='patient ID (eg, p000188)', required=True)
    parser.add_argument('-i', '--idx', type=int, help='segment index', required=True)
    args = parser.parse_args()

    fs = 125  # Sampling frequency

    # 1. Load Raw Data
    print(f"Loading data for Patient {args.patient}, Segment {args.idx}...")
    raw_ecg = load_signal(args.dbPath, args.patient, args.idx, 'ecg')
    raw_ppg = load_signal(args.dbPath, args.patient, args.idx, 'ppg')

    # 2. Preprocess (Bandpass + Z-score)
    print("Preprocessing signals...")
    clean_ecg, clean_ppg = preprocess_segment(raw_ecg, raw_ppg, fs=fs)

    # 3. Extract Fiducial Points
    print("Extracting peaks...")
    ecg_r_peaks = get_peaks(clean_ecg, fs=fs)
    ppg_peaks = get_peaks(clean_ppg, fs=fs)
    # Extract the P-waves using the R-peaks as anchors
    ecg_p_peaks = get_p_peaks(clean_ecg, ecg_r_peaks, fs=fs)

    # 4. Calculate Delays
    avg_pat = calculate_pat(ecg_r_peaks, ppg_peaks, fs=fs)
    avg_ptt = calculate_ptt(ecg_p_peaks, ppg_peaks, fs=fs)
    print(f"\n---> Calculated Average PAT (R-peak to PPG): {avg_pat:.2f} ms")
    print(f"---> Calculated Average PTT (P-peak to PPG): {avg_ptt:.2f} ms <---")

    # 5. Visual Check
    print("Generating visual check graph...")
    N = len(clean_ecg)
    t = np.arange(N) / fs
    mask = t < 5.0

    ecg_r_plot = ecg_r_peaks[ecg_r_peaks < (5.0 * fs)]
    ecg_p_plot = ecg_p_peaks[ecg_p_peaks < (5.0 * fs)]
    ppg_plot = ppg_peaks[ppg_peaks < (5.0 * fs)]

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

    # Plot ECG with R-peaks and P-peaks
    ax1.plot(t[mask], clean_ecg[mask], label='Filtered ECG', color='blue')
    ax1.plot(t[ecg_r_plot], clean_ecg[ecg_r_plot], "ro", label='R-Peaks')
    ax1.plot(t[ecg_p_plot], clean_ecg[ecg_p_plot], "yo", markersize=8, label='P-Peaks')  # Yellow dots for P-waves
    ax1.set_ylabel('Amplitude (Z-score)')
    ax1.set_title(f'Peak Detection - Patient {args.patient}, Seg {args.idx}')
    ax1.legend(loc='upper right')
    ax1.grid(True)

    # Plot PPG
    ax2.plot(t[mask], clean_ppg[mask], label='Filtered PPG', color='green')
    ax2.plot(t[ppg_plot], clean_ppg[ppg_plot], "ro", label='Systolic Peaks')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_ylabel('Amplitude (Z-score)')
    ax2.legend(loc='upper right')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()