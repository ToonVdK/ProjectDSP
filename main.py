r"""
Example usage:
>  python main.py -d C:\Users\vande\PycharmProjects\DSP\ProjectBPAnalysis\data\ -p p000188 -i 1
>  python main.py -d C:\Users\vande\PycharmProjects\DSP\ProjectBPAnalysis\data\ -p p000188 -a
"""
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

# Import functions from the other files
from preprocess import preprocess_segment
from extract_features import get_peaks, get_p_peaks, calculate_pat, calculate_ptt
from extract_features import get_peaks, calculate_pat, get_p_peaks, calculate_ptt, calculate_heart_rate


def load_signal(dbPath, patient, idx, signal_type):
    """Utility to load a specific raw signal segment."""
    file_path = os.path.join(dbPath, f"{patient}_{signal_type}.npy")
    wave = np.load(file_path)
    return wave[idx]

def process_segment(dbPath, patient, idx, fs=125, plot=False):
    """
        Processes a single segment and returns its metrics. 
    """
    raw_ecg = load_signal(dbPath, patient, idx, 'ecg')
    raw_ppg = load_signal(dbPath, patient, idx, 'ppg')

    # --- PREPROCESS ---
    clean_ecg, clean_ppg = preprocess_segment(raw_ecg, raw_ppg, fs=fs)

    # --- EXTRACT PEAKS ---
    ecg_r_peaks = get_peaks(clean_ecg, fs=fs)
    ppg_peaks = get_peaks(clean_ppg, fs=fs)
    ecg_p_peaks = get_p_peaks(clean_ecg, ecg_r_peaks, fs=fs)

    # --- CALCULATE METRICS ---
    ecg_hr = calculate_heart_rate(ecg_r_peaks, fs=fs)
    ppg_hr = calculate_heart_rate(ppg_peaks, fs=fs)
    avg_pat = calculate_pat(ecg_r_peaks, ppg_peaks, fs=fs)
    avg_ptt = calculate_ptt(ecg_p_peaks, ppg_peaks, fs=fs)

    # Optional plotting for debugging single segments
    if plot:
        N = len(clean_ecg)
        t = np.arange(N) / fs
        mask = t < 5.0

        ecg_r_plot = ecg_r_peaks[ecg_r_peaks < (5.0 * fs)]
        ecg_p_plot = ecg_p_peaks[ecg_p_peaks < (5.0 * fs)]
        ppg_plot = ppg_peaks[ppg_peaks < (5.0 * fs)]

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

        # Plot ECG with R-peaks and P-peaks
        ax1.plot(t[mask], clean_ecg[mask], label='Filtered ECG', color='blue')
        ax1.plot(t[ecg_r_plot], clean_ecg[ecg_r_plot], "ro", label='R-Peaks', markersize=4)
        ax1.plot(t[ecg_p_plot], clean_ecg[ecg_p_plot], "yo", label='P-Peaks', markersize=4)  # Yellow dots for P-waves
        ax1.set_ylabel('Amplitude (Z-score)')
        ax1.set_title(f'Peak Detection - Patient {patient}, Seg {idx}')
        ax1.legend(loc='upper right')
        ax1.grid(True)

        # Plot PPG
        ax2.plot(t[mask], clean_ppg[mask], label='Filtered PPG', color='green')
        ax2.plot(t[ppg_plot], clean_ppg[ppg_plot], "ro", label='Systolic Peaks', markersize=4)
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Amplitude (Z-score)')
        ax2.legend(loc='upper right')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

    return {
        'segment': idx,
        'ecg_hr': ecg_hr,
        'ppg_hr': ppg_hr,
        'pat': avg_pat,
        'ptt': avg_ptt
    }


def main():
    parser = argparse.ArgumentParser(description='Run BP extraction pipeline.')
    parser.add_argument('-d', '--dbPath', help='path to .npy files', required=True)
    parser.add_argument('-p', '--patient', help='patient ID (eg, p000188)', required=True)
    parser.add_argument('-i', '--idx', type=int, help='segment index', default=None)
    parser.add_argument('-a', '--all', action='store_true', help='Process all segments for the patient')
    args = parser.parse_args()

    fs = 125  # Sampling frequency

    if args.all:
        print(f"Processing ALL segments for Patient {args.patient}...")
        results = []

        # The dataset has 30 segments per patient (indices 0 to 29)
        for i in range(30):
            try:
                metrics = process_segment(args.dbPath, args.patient, i, fs=fs, plot=False)
                # Only save results if the algorithm actually found valid PAT/PTT values (not NaN)
                if not np.isnan(metrics['pat']) and not np.isnan(metrics['ptt']):
                    results.append(metrics)
            except Exception as e:
                print(f"Skipping segment {i} due to error/bad data.")

        # --- Calculate and Print Statistics ---
        if results:
            all_pat = [res['pat'] for res in results]
            all_ptt = [res['ptt'] for res in results]
            all_ecg_hr = [res['ecg_hr'] for res in results]
            all_ppg_hr = [res['ppg_hr'] for res in results]

            mean_ecg_hr = np.mean(all_ecg_hr)
            mean_ppg_hr = np.mean(all_ppg_hr)
            hr_diff = abs(mean_ecg_hr - mean_ppg_hr)

            print("\n" + "=" * 50)
            print(f"STATISTICS: PATIENT {args.patient}")
            print("=" * 50)
            print(f"Segments Processed Successfully: {len(results)}/30")
            print(f"Mean ECG HR: {mean_ecg_hr:.2f} BPM")
            print(f"Mean PPG HR: {mean_ppg_hr:.2f} BPM")
            print(f"Average HR Difference: {hr_diff:.2f} BPM")
            print("-" * 50)
            print(f"Mean PAT: {np.mean(all_pat):.2f} ms (Std Dev: {np.std(all_pat):.2f} ms)")
            print(f"Mean PTT: {np.mean(all_ptt):.2f} ms (Std Dev: {np.std(all_ptt):.2f} ms)")
            print("=" * 50 + "\n")
        else:
            print("No valid segments found to calculate statistics.")
    elif args.idx is not None:
        # Run just one segment and print the details (like we did before)
        metrics = process_segment(args.dbPath, args.patient, args.idx, fs=fs, plot=True)
        print(metrics)
    else:
        print("Please provide either a segment index (-i) or use the --all flag (-a).")


if __name__ == '__main__':
    main()