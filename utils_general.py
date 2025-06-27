import os

import glob
import subprocess
from multiprocessing import Pool
import matplotlib.pyplot as plt

import numpy as np
import nibabel as nib

#import vtk # alla fine non usato
import SimpleITK as sitk



def check_files(pattern, list = False):
    files = glob.glob(pattern)
    count = len(files)
    if not files:
        print(f"0 files found for pattern: {pattern}")
    else: 
        print(f"{count} Files found for pattern: {pattern}")
        if list:
            for file in files:
                print(file)



def run_commands_parallel(commands, num_processes=None): # none means use all available cores
    """Executes a list of commands in parallel using multiprocessing."""
    with Pool(processes=num_processes) as pool:
        pool.map(run_command, commands)

def run_command(command):
    print(f" ========= RUN command: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        pass
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")


def convert_nrrd_to_nii(folder_path):
    """Convert all .nrrd files in a folder to .nii.gz format."""
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return
    
    for file in os.listdir(folder_path):
        if file.endswith(".nrrd"):
            nrrd_path = os.path.join(folder_path, file)
            nii_path = os.path.join(folder_path, file.replace(".nrrd", ".nii.gz")) # just replace the extension

            try:
                img = sitk.ReadImage(nrrd_path)
                sitk.WriteImage(img, nii_path)
                print(f"Converted: {nrrd_path} -> {nii_path}")
            except Exception as e:
                print(f"Failed to convert {nrrd_path}: {e}")
        
def read_from_nrrd(file):
    img = sitk.ReadImage(file)
    data = sitk.GetArrayFromImage(img)
    return data

def reduce4thDim(file):
    img = nib.load(file)
    img_data = img.get_fdata()
    print(img_data.shape)
    # Remove singleton dimension (4th dimension)
    img_data_fixed = np.squeeze(img_data, axis=3)  # Remove dimension at index 3
    print(img_data_fixed.shape)
    # Save the fixed NIfTI file
    new_img = nib.Nifti1Image(img_data_fixed, img.affine, img.header)
    resid_fixed = f"{file.replace('.nii.gz', '_fixed.nii.gz')}"
    nib.save(new_img, resid_fixed)
    return resid_fixed

def convert_from_afni_to_nifti(file):
    file_converted = file.replace('+orig', '.nii.gz')
    # 3dcopy
    command = f"3dcopy {file} {file_converted}"
    print(command)
    run_command(command)
    return file_converted

def convert_to_orig(file):
    file_converted_orig = file.replace('.nii.gz', '+orig') # default it creates .tlrc file
    # 3dcopy
    command = f"3dcopy {file} {file_converted_orig}"
    print(command)
    run_command(command)
    return file_converted_orig


def plot_nifti_slices(input_pattern, layer_max=60, step=10, num_files_limit=40, cmap='gray'):
    files = sorted(glob.glob(input_pattern))[:num_files_limit]  # Select the first 'num_files'
    # exclude containing "dyrk"
    #files = [f for f in files if "dyrk" not in f]
    if not files:
        print("No files found with the given pattern.")
        return
    # exclude containing "slices"
    files = [f for f in files if "slices" not in f]

    num_files = len(files)
    layers = layer_max // step +1  # step of 10 layers for each file
    
    fig, axs = plt.subplots(num_files, layers, figsize=(50, 4 * num_files))
    
    for i, file in enumerate(files):
        # if nrrd
        if file.endswith('.nrrd'):
            data = read_from_nrrd(file)
            filename = os.path.basename(file)
            # put first dimension in the last
            data = np.moveaxis(data, 0, -1)

        else:
            img = nib.load(file)
            filename = os.path.basename(file)
            data = img.get_fdata()
        #print shape
        print(f"{filename} shape: {data.shape}")

        #layers_max_current = data.shape[2]
        layers_max_current = min(layer_max, data.shape[2])  # Use the minimum of layer_max or actual depth
        layers_current = layers_max_current // step +1

        for j in range(layers_current):
            layer_idx = min(j * step, data.shape[2] - 1)  # Ensure we don't exceed data dimensions
            axs[i, j].imshow(data[:, :, layer_idx], cmap=cmap)
            # filename and shape
            axs[i, j].set_title(f"{filename}\nShape: {data.shape}\nLayer: {j * step}")
            axs[i, j].axis('off')
    
    plt.tight_layout()
    dir = os.path.dirname(file)
    # take before the last /
    
    # one level up dir 
    
    #plt.savefig(f"{os.path.dirname(file)}/nifti_slices.png")#, dpi=300)
    plt.savefig(f"{os.path.dirname(file)}/image_slices.pdf")
    
    
    #plt.show()



import re
import datetime
# Function to convert seconds to HH:MM:SS format

def convert_seconds_to_hms(seconds):
    # remove decimals
    return str(datetime.timedelta(seconds=seconds)).split(".")[0]

def convert_file_seconds(filename): 
    # Process the log file
    converted_lines = []
    with open(filename, "r") as file:
        for line in file:
            # Replace all numbers with a dot by converting them to HH:MM:SS format
            # if no dot, it will not be converted
            converted_line = re.sub(r"\b\d+\.\d+\b", lambda x: convert_seconds_to_hms(float(x.group())), line.strip())
            converted_lines.append(converted_line)

    # Save the converted log file
    #output_file_path = "time.log"
    output_file_path = filename.replace(".log", "_converted.log")
    # same 
    #output_file_path = filename
    with open(output_file_path, "w") as file:
        file.write("\n".join(converted_lines))

    print(f"Conversion complete. Output saved to {output_file_path}")

