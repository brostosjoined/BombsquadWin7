# -*- coding: utf-8 -*-

import os
import threading
import time
import requests
import zipfile
import platform
import webbrowser
import shutil
import pefile
import sys

major = None
minor = None



def find_python_dll(current_dir):
    """Finds a DLL file in the current directory starting with 'python' and ending with '.dll'."""
    for filename in os.listdir(current_dir):
        if filename.lower().startswith("python") and filename.lower().endswith(".dll"):
            return os.path.join(current_dir, filename)
    raise FileNotFoundError(
        "Please place this exe in the folder containing bombsquad executable and for the server place it inside dist folder."
    )


def get_dll_product_version(dll_path):
    """Extracts and returns the product version and architecture from the DLL file."""
    with pefile.PE(dll_path) as pe:
        if not hasattr(pe, "VS_FIXEDFILEINFO"):
            raise Exception("No version information found in the DLL.")

        version_info = pe.VS_FIXEDFILEINFO[0]
        product_version = (
            version_info.ProductVersionMS >> 16,
            version_info.ProductVersionMS & 0xFFFF,
            version_info.ProductVersionLS >> 16,
            version_info.ProductVersionLS & 0xFFFF,
        )
        is_64bit = pe.FILE_HEADER.Machine in (
            pefile.MACHINE_TYPE["IMAGE_FILE_MACHINE_AMD64"],
            pefile.MACHINE_TYPE["IMAGE_FILE_MACHINE_IA64"],
        )
        architecture = "amd64" if is_64bit else "win32"

        return product_version, architecture


def format_version(version):
    """Formats the version tuple to a string in the format Major.Minor.Build."""
    global major, minor
    major, minor, build, _ = version
    major = major
    minor = minor
    return f"{major}.{minor}.{build // 1000}"


def try_download_zip(version, architecture):
    """Attempts to download and save the ZIP file from GitHub."""
    base_url_template = f"https://github.com/adang1345/PythonWin7/raw/master/{version}/python-{version}-embed-{architecture}.zip"
    url = base_url_template.format(version=version, architecture=architecture)
    # print(f"Attempting to download ZIP from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()

        # if "application/zip" not in response.headers.get("Content-Type", ""):
        #     print("Warning: The content type is not 'application/zip'.")

        zip_filename = f"python-{version}-embed-{architecture}.zip"
        # print(f"Saving ZIP file as: {zip_filename}")
        with open(zip_filename, "wb") as f:
            f.write(response.content)
        # print(time.ctime())

        # if response.content[:4] != b"PK\x03\x04":
        #     print("Warning: The file does not appear to be a valid ZIP file.")
        # else:
        #     print("ZIP file downloaded and saved successfully.")

        return zip_filename
    except requests.HTTPError as e:
        # print(f"Failed to download from {url}: {e}")
        raise Exception(f"{e}")
    except Exception as e:
        # print(f"Error while saving the ZIP file: {e}")
        raise Exception(f"{e}")


def extract_zip(zip_path, extract_to):
    """Extracts a ZIP file to the specified directory."""
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def copy_files(src_folder, dest_folder, filenames):
    """Copies specified files from source folder to destination folder."""
    for filename in filenames:
        src_file = os.path.join(src_folder, filename)
        dest_file = os.path.join(dest_folder, filename)
        if os.path.exists(src_file):
            try:
                shutil.copyfile(src_file, dest_file)
                # print(f"Copied {filename} from {src_folder} to {dest_folder}")
            except Exception as e:
                raise Exception(f"{e}")
        # else:
        #     print(f"File {filename} not found in {src_folder}")


def clean_up_files(files_to_delete):
    """Deletes specified files."""
    for file_path in files_to_delete:
        if os.path.exists(file_path):
            os.remove(file_path)
        #     print(f"Deleted {file_path}")
        # else:
        #     print(f"File {file_path} not found")


def clean_up_folder(folder_path):
    """Deletes a folder and all its contents."""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    #     print(f"Deleted folder {folder_path}")
    # else:
    #     print(f"Folder {folder_path} not found")

duration = 1
def loading_animation():
    spinner = ['|', '/', '-', '\\']
    while duration == 1:
        for i in range(duration * 10):  # duration * 10 gives you roughly the duration in seconds
            sys.stdout.write(f"\rPatching... {spinner[i % len(spinner)]}")
            sys.stdout.flush()
            time.sleep(0.1)
    else:
        return

def main():

    try:
        
        if platform.release() != "7":
            print("Works on Windows 7 only.")
            os.system("pause")
            sys.exit(1)
            
        global duration 
        threading.Thread(target=loading_animation).start()
        # Get the current working directory
        cwd = os.getcwd()
        # cwd = "C:\\Users\\user\\Desktop\\Inventory\\Games\\Bombsquad\\BombSquad_Windows_1.7.37"

        # Find the DLL file
        dll_path = find_python_dll(cwd)
        # print(f"Found DLL: {dll_path}")

        # Get and print the product version and architecture
        version, architecture = get_dll_product_version(dll_path)
        version_str = format_version(version)
        # print(f"Product Version: {version_str}")
        # print(f"Architecture: {architecture}")
        if minor < 9:
            duration = 0
            time.sleep(1)
            print(
                f"Please download latest version of BombSquad."
            )
            os.system("pause")
            sys.exit()

        # Try downloading and saving the ZIP file
        zip_file = try_download_zip(version_str, architecture)
        # zip_file = os.path.join(cwd, "python-3.12.3-embed-win32.zip")
        if not zip_file:
            print(
                f"Unable to download the ZIP file for the specified version."
            )

        # Define paths
        dll_folder = os.path.join(cwd, "DLLs")
        lib_folder = os.path.join(cwd, "lib")

        # Step 1: Extract the ZIP file to the DLLs folder
        # print("Extracting ZIP file to DLLs folder...")
        extract_zip(zip_file, dll_folder)

        # Step 2: Copy specific DLL files from DLLs folder to the current working directory
        # print("Copying DLL files to current directory...")

        copy_files(
            dll_folder,
            cwd,
            ["api-ms-win-core-path-l1-1-0.dll", f"python{major}{minor}.dll"],
        )
        server = os.path.join(cwd, "python.exe")
        if server:
            copy_files(dll_folder, cwd, ["python.exe"])
            clean_up_folder(lib_folder)
            os.makedirs(lib_folder)

        # Step 3: Extract the Python ZIP file into the lib folder
        libs_zip = os.path.join(dll_folder, f"python{major}{minor}.zip")
        # print(f"Extracting {zip_file} to lib folder...")
        extract_zip(libs_zip, lib_folder)

        # Step 4: Clean up - Delete specific files and folders
        # print("Cleaning up files and folders...")
        clean_up_files(
            [
                zip_file,
                libs_zip,
                os.path.join(dll_folder, f"python{major}.dll"),
                os.path.join(dll_folder, f"python{major}{minor}.dll"),
                os.path.join(dll_folder, "api-ms-win-core-path-l1-1-0.dll"),
                os.path.join(dll_folder, "pythonw.exe"),
                os.path.join(dll_folder, "python.exe"),
                os.path.join(dll_folder, "python312._pth"),
            ]
        )

        # Clean up _pycache_ in lib folder
        clean_up_folder(os.path.join(lib_folder, "__pycache__"))
        duration = 0
        time.sleep(1)
        print(f"Patching Successful.\nMade to you by brostos.")
        webbrowser.open("https://github.com/brostosjoined/BombsquadWin7")
        os.system("pause")

    except Exception as e:
        duration = 0
        time.sleep(1)
        print(f"Error: {e}")
        os.system("pause")
        


if __name__ == "__main__":
    main()
