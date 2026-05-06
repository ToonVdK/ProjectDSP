import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Import your existing preprocess function
from preprocess import preprocess_segment


def plot_pan_tompkins_stages(clean_ecg, fs=125, zoom_sec=5.0):
    """
    Visualizes the internal mathematical steps of the Pan-Tompkins algorithm.
    zoom_sec: Limits the plot to the first few seconds so the waves are visible.
    """
    # --- STEP 1: Differentiation (to find steep slopes) ---
    diff_ecg = np.diff(clean_ecg)
    diff_ecg = np.append(diff_ecg, 0)

    # --- STEP 2: Squaring (to suppress P/T waves and enhance QRS) ---
    squared_ecg = diff_ecg ** 2

    # --- STEP 3: Integration (to create the "lumps") ---
    window_width = int(0.15 * fs)
    integrated_ecg = np.convolve(squared_ecg, np.ones(window_width) / window_width, mode='same')

    # --- STEP 4: Peak Detection (recreating your exact logic) ---
    threshold = 2.5 * np.mean(integrated_ecg)
    qrs_lumps, _ = find_peaks(integrated_ecg, height=threshold, distance=int(0.3 * fs))

    r_peaks = []
    search_window = int(0.1 * fs)
    for lump in qrs_lumps:
        start = max(0, lump - search_window)
        end = min(len(clean_ecg), lump + search_window)
        if start < end:
            actual_r = start + np.argmax(clean_ecg[start:end])
            r_peaks.append(actual_r)
    r_peaks = np.unique(r_peaks)

    # =========================================================
    # PLOTTING
    # =========================================================
    N = len(clean_ecg)
    t = np.arange(N) / fs
    mask = t < zoom_sec  # Mask to zoom in on the timeline

    # Create 4 stacked subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(10, 10))

    # Plot 1: Filtered ECG
    ax1.plot(t[mask], clean_ecg[mask], color='blue')
    ax1.set_title('1. Filtered ECG (Notice the smaller P and T waves)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True)

    # Plot 2: Squared Derivative
    ax2.plot(t[mask], squared_ecg[mask], color='purple')
    ax2.set_title('2. Squared Derivative (P and T waves are suppressed)')
    ax2.set_ylabel('Amplitude²')
    ax2.grid(True)

    # Plot 3: Moving Window Integration
    ax3.plot(t[mask], integrated_ecg[mask], color='orange')
    ax3.axhline(threshold, color='red', linestyle='--', label='Adaptive Threshold')
    ax3.set_title('3. Moving Window Integration (QRS complexes become "lumps")')
    ax3.set_ylabel('Energy')
    ax3.legend(loc='upper right')
    ax3.grid(True)

    # Plot 4: Final ECG with R-peaks
    r_peaks_plot = [p for p in r_peaks if t[p] < zoom_sec]
    ax4.plot(t[mask], clean_ecg[mask], color='blue')
    ax4.plot(t[r_peaks_plot], clean_ecg[r_peaks_plot], "ro", label='Detected R-Peaks', markersize=6)
    ax4.set_title('4. Final Signal Search (Original R-peak located inside the lump window)')
    ax4.set_ylabel('Amplitude')
    ax4.set_xlabel('Time (seconds)')
    ax4.legend(loc='upper right')
    ax4.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # 1. Define your paths (Update this to your actual data folder)
    dbPath = r"C:\Users\vande\PycharmProjects\DSP\ProjectBPAnalysis\data\\"
    patient = "p006621"  # Pick a patient with a clean ECG
    idx = 15  # Pick segment 0

    # 2. Load the raw signals
    raw_ecg = np.load(os.path.join(dbPath, f"{patient}_ecg.npy"))[idx]
    raw_ppg = np.load(os.path.join(dbPath, f"{patient}_ppg.npy"))[idx]

    # 3. Get the clean ECG using your existing pipeline
    clean_ecg, clean_ppg = preprocess_segment(raw_ecg, raw_ppg, fs=125)

    # 4. Generate the plot
    plot_pan_tompkins_stages(clean_ecg, fs=125, zoom_sec=5.0)