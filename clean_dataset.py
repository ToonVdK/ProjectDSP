import os
import shutil
import numpy as np
import glob
from main import process_segment


def curate_database(dbPath):
    # Create a folder for the rejected patients
    rejected_dir = os.path.join(dbPath, "rejected")
    if not os.path.exists(rejected_dir):
        os.makedirs(rejected_dir)
        print(f"Created quarantine folder at: {rejected_dir}")

    # Find all unique patient IDs in the data folder
    # We look for files ending in '_ecg.npy' and split the filename to get the ID
    search_pattern = os.path.join(dbPath, '*_ecg.npy')
    patient_files = glob.glob(search_pattern)

    patient_ids = []
    for file_path in patient_files:
        filename = os.path.basename(file_path)
        patient_id = filename.split('_')[0]
        patient_ids.append(patient_id)

    print(f"Found {len(patient_ids)} total patients in dataset. Beginning curation...\n")

    valid_count = 0
    rejected_count = 0

    # Test Segment 0 for every patient
    for patient in patient_ids:
        try:
            # Set plot=False so we don't get 100 pop-up windows
            metrics = process_segment(dbPath, patient, 0, fs=125, plot=False)

            # Calculate the physiological rules
            hr_diff = abs(metrics['ecg_hr'] - metrics['ppg_hr'])
            is_nan = np.isnan(metrics['pat']) or np.isnan(metrics['ptt']) or np.isnan(metrics['ecg_hr'])

            # The Time Travel Paradox rule
            physiologically_impossible = metrics['pat'] >= metrics['ptt']

            # Evaluate
            if is_nan or hr_diff > 5.0 or physiologically_impossible:
                reason = "NaNs/Noise" if is_nan else (
                    "HR Mismatch" if hr_diff > 5.0 else "PAT >= PTT")
                print(f"[-] REJECTED {patient}: {reason}. Moving files...")
                move_patient_files(dbPath, rejected_dir, patient)
                rejected_count += 1
            else:
                print(f"[+] ACCEPTED {patient}: Physiologically valid.")
                valid_count += 1

        except Exception as e:
            print(f"[-] REJECTED {patient}: Code Error ({e}). Moving files...")
            move_patient_files(dbPath, rejected_dir, patient)
            rejected_count += 1

    # Print final summary
    print("\n" + "=" * 50)
    print("DATASET CURATION COMPLETE")
    print("=" * 50)
    print(f"Total Patients Analyzed: {len(patient_ids)}")
    print(f"Valid Patients Kept:     {valid_count}")
    print(f"Invalid Patients Moved:  {rejected_count}")
    print("=" * 50)


def move_patient_files(src_dir, dest_dir, patient_id):
    """
    Helper function to safely move all 3 files (_ecg, _ppg, _labels)
    for a given patient into the rejected folder.
    """
    suffixes = ['_ecg.npy', '_ppg.npy', '_labels.npy']

    for suffix in suffixes:
        src_file = os.path.join(src_dir, f"{patient_id}{suffix}")
        dest_file = os.path.join(dest_dir, f"{patient_id}{suffix}")

        # Only move it if it actually exists in the source folder
        if os.path.exists(src_file):
            shutil.move(src_file, dest_file)


if __name__ == '__main__':
    # Define your data path here
    data_folder = r"C:\Users\vande\PycharmProjects\DSP\ProjectBPAnalysis\data\\"

    curate_database(data_folder)