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
from preprocess import preprocess_segment, plot_pre_post_processing
from extract_features import *


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
    ecg_r_peaks = pan_tompkins_r_peaks(clean_ecg, fs=fs)
    ppg_peaks = get_peaks(clean_ppg, fs=fs)

    # --- CALCULATE METRICS ---
    ecg_hr = calculate_heart_rate(ecg_r_peaks, fs=fs)
    ppg_hr = calculate_heart_rate(ppg_peaks, fs=fs)
    ecg_sdnn, ecg_rmssd = calculate_hrv(ecg_r_peaks, fs=fs)
    ppg_sdnn, ppg_rmssd = calculate_hrv(ppg_peaks, fs=fs)

    # --- SIGNAL QUALITY & FUSION
    ecg_sqi = calculate_sqi(clean_ecg, ecg_r_peaks, fs=fs)
    ppg_sqi = calculate_sqi(clean_ppg, ppg_peaks, fs=fs)
    fused_hr, w_ecg, w_ppg = fuse_heart_rates(ecg_hr, ppg_hr, ecg_sqi, ppg_sqi)

    fused_sdnn = (w_ecg * ecg_sdnn) + (w_ppg * ppg_sdnn)
    fused_rmssd = (w_ecg * ecg_rmssd) + (w_ppg * ppg_rmssd)

    # Optional plotting for debugging single segments
    if plot:
        plot_pre_post_processing(raw_ecg, clean_ecg, fs=fs, signal_name="ECG")
        plot_pre_post_processing(raw_ppg, clean_ppg, fs=fs, signal_name="PPG")

        N = len(clean_ecg)
        t = np.arange(N) / fs
        mask = t < 5.0

        ecg_r_plot = ecg_r_peaks[ecg_r_peaks < (5.0 * fs)]
        ppg_plot = ppg_peaks[ppg_peaks < (5.0 * fs)]

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

        # Plot ECG with R-peaks and P-peaks
        ax1.plot(t[mask], clean_ecg[mask], label='Filtered ECG', color='blue')
        ax1.plot(t[ecg_r_plot], clean_ecg[ecg_r_plot], "ro", label='R-Peaks', markersize=4)
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
        'ecg_hr': ecg_hr, 'ppg_hr': ppg_hr, 'fused_hr': fused_hr,
        'ecg_sqi': ecg_sqi, 'ppg_sqi': ppg_sqi, 'w_ecg': w_ecg, 'w_ppg': w_ppg,
        'ecg_sdnn': ecg_sdnn, 'ppg_sdnn': ppg_sdnn, 'fused_sdnn': fused_sdnn,
        'ecg_rmssd': ecg_rmssd, 'ppg_rmssd': ppg_rmssd, 'fused_rmssd': fused_rmssd
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
        print(f"Processing first segment for Patient {args.patient}...")
        results = []

        # The dataset has 30 segments per patient (indices 0 to 29)
        # We only take the first segment due to the PPG drifting over time.
        for i in range(30):
            try:
                metrics = process_segment(args.dbPath, args.patient, i, fs=fs, plot=False)

                # Check if any of our crucial metrics returned NaN
                if np.isnan(metrics['ecg_hr']) or np.isnan(metrics['ppg_hr']) or np.isnan(metrics['fused_hr']):
                    print(f"[-] Skipped Segment {i:02d}: Rejected due to NaN (No valid peaks found).")
                else:
                    print(f"[+] Segment {i:02d} processed successfully. (Fused HR: {metrics['fused_hr']:.1f} BPM)")
                    results.append(metrics)

            except Exception as e:
                print(f"[-] Skipped Segment {i:02d}: Code execution error -> {e}")

        # --- Calculate and Print Statistics ---
        if results:
            mean_ecg_hr = np.mean([res['ecg_hr'] for res in results])
            mean_ppg_hr = np.mean([res['ppg_hr'] for res in results])
            mean_ecg_sqi = np.mean([res['ecg_sqi'] for res in results])
            mean_ppg_sqi = np.mean([res['ppg_sqi'] for res in results])
            mean_w_ecg = np.mean([res['w_ecg'] for res in results])
            mean_w_ppg = np.mean([res['w_ppg'] for res in results])

            mean_fused_hr = np.mean([res['fused_hr'] for res in results])

            # Average HRV Metrics
            mean_fused_sdnn = np.mean([res['fused_sdnn'] for res in results])
            mean_fused_rmssd = np.mean([res['fused_rmssd'] for res in results])

            print("\n" + "=" * 65)
            print(f"STATISTICS: PATIENT {args.patient} (OVERALL 15-MIN AVERAGES)")
            print("=" * 65)
            print(f"Valid Segments Processed: {len(results)}/30")
            print("-" * 65)
            print(f"Avg ECG:  HR: {mean_ecg_hr:5.1f} BPM  |  SQI: {mean_ecg_sqi:.2f}  |  Weight: {mean_w_ecg:.2f}")
            print(f"Avg PPG:  HR: {mean_ppg_hr:5.1f} BPM  |  SQI: {mean_ppg_sqi:.2f}  |  Weight: {mean_w_ppg:.2f}")
            print("-" * 65)
            print(f"FUSED HEART RATE: {mean_fused_hr:.1f} BPM")
            print(f"FUSED HRV (SDNN):  {mean_fused_sdnn:.1f} ms")
            print(f"FUSED HRV (RMSSD): {mean_fused_rmssd:.1f} ms")
            print("=" * 65 + "\n")
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