import os
import zipfile

SOURCE_FOLDER = r"C:\Users\Willow\Downloads\Sonniss"
DESTINATION_FOLDER = r"E:\SampleAudioFiles"

os.makedirs(DESTINATION_FOLDER, exist_ok=True)

for file_name in os.listdir(SOURCE_FOLDER):
    if file_name.lower().endswith(".zip"):
        zip_path = os.path.join(SOURCE_FOLDER, file_name)

        # Create a folder with the same name as the zip file (without .zip)
        extract_folder_name = os.path.splitext(file_name)[0]
        extract_path = os.path.join(DESTINATION_FOLDER, extract_folder_name)

        os.makedirs(extract_path, exist_ok=True)

        print(f"Extracting: {zip_path}")
        print(f"To: {extract_path}")

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)

print("Done extracting all zip files.")