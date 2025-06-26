# ruff: noqa: F403 F405 F401 
import os
import glob

import subprocess
from multiprocessing import Pool
from multiprocessing import get_context # for macos

import nibabel as nib
import numpy as np

import matplotlib.pyplot as plt

from utils_general import *
from utils_reg import *


# fslmaths needs this
os.environ["FSLDIR"] = os.environ["CONDA_PREFIX"]
os.environ["FSLOUTPUTTYPE"] = "NIFTI_GZ"  #  default output type for fslmaths 
#os.environ["NODE_OPTIONS"] = "--max_old_space_size=8192"
#os.environ["NODE_OPTIONS"] = "--max-old-space-size=8192 --experimental-worker"


def make_folder(folder):
    """Create a folder if it does not exist and return its path."""
    os.makedirs(folder, exist_ok=True)
    return folder

def process_file(file_path):
    """Full processing pipeline for a single file using BisWeb."""
    #file_base = os.path.basename(file_path).replace("_C0__optfixed.nii.gz", "")
    file_base = os.path.basename(file_path).replace("_C0.nrrd", "")

    nrrd_c0 = f"{nrrd_folder}/{file_base}_C0.nrrd"
    nrrd_c1 = f"{nrrd_folder}/{file_base}_C1.nrrd"

    opt_c0 = f"{opt_folder}/{file_base}_C0__optfixed.nii.gz"
    opt_c1 = f"{opt_folder}/{file_base}_C1__optfixed.nii.gz"
    opt_c2 = f"{opt_folder}/{file_base}_C2__optfixed.nii.gz"

    bisxform_file = f"{xform_folder}/standard_ref__{file_base}_C1__optfixed__nlr.bisxform"
    
    registered_c0_file = f"{reg_folder}/r_{file_base}_C0__optfixed.nii.gz"
    registered_c1_file = f"{reg_folder}/r_{file_base}_C1__optfixed.nii.gz"
    registered_c2_file = f"{reg_folder}/r_{file_base}_C2__optfixed.nii.gz"

    divided_c0_file = f"{div_c0_folder}/r_{file_base}_C0divC1.nii.gz"
    divided_c2_file = f"{div_c2_folder}/r_{file_base}_C2divC1.nii.gz"

    jacobian_file = f"{jacob_folder}/ja_{file_base}.nii.gz"
    mask_file = f"{jacob_folder}/mask_ja_{file_base}.nii.gz"

    # Preprocess images
    preprocess(nrrd_c0, opt_c0)
    preprocess(nrrd_c1, opt_c1)

    # Perform non-linear registration
    # Check if the file already exists - this is the heaviest step 
    nonlinear_registration(opt_c1, non_param_file, STANDARD_REFERENCE, bisxform_file)

    # Reslice images
    reslice_image(opt_c1, STANDARD_REFERENCE, bisxform_file, registered_c1_file)
    reslice_image(opt_c0, registered_c1_file, bisxform_file, registered_c0_file)
    if os.path.isfile(opt_c2):
        reslice_image(opt_c2, registered_c1_file, bisxform_file, registered_c2_file)

    # Perform division
    divide_images(registered_c0_file, registered_c1_file, divided_c0_file)
    if os.path.isfile(opt_c2):
        divide_images(registered_c2_file, registered_c1_file, divided_c2_file)

    # Compute Jacobian
    compute_jacobian(bisxform_file, STANDARD_RSP_REFERENCE, jacobian_file)

    # Apply mask
    apply_mask(jacobian_file, DIS_ATLAS_MASK_FILE, mask_file)



if __name__ == "__main__":
    
    # INPUT
    experiment_folder = 'data/data_dyrka'
    # INPUT

    non_param_file = "aux/01-reg/nonlinearRegistration.param"
    # Define paths
    STANDARD_REFERENCE = "aux/01-reg/standard_ref.nii.gz"
    STANDARD_RSP_REFERENCE = "aux/01-reg/standard_ref_rsp.nii.gz"
    DIS_ATLAS_MASK_FILE = "aux/01-reg/dis_atlas_mask.nii.gz"

    # Define folders
    nrrd_folder = make_folder(f"{experiment_folder}/nrrd") # input nrrd files
    opt_folder = make_folder(f"{experiment_folder}/optfixed")
    xform_folder = make_folder(f"{experiment_folder}/xform")
    reg_folder = make_folder(f"{experiment_folder}/registered")
    div_c0_folder = make_folder(f"{experiment_folder}/divided/C0divC1")
    div_c2_folder = make_folder(f"{experiment_folder}/divided/C2divC1") # only used if C2 is present
    jacob_folder = make_folder(f"{experiment_folder}/jacobian")


    # Get nrrd files only C0
    input_pattern = f"{experiment_folder}/nrrd/*C0.nrrd"
    files = sorted(glob.glob(input_pattern))
    # Parallel execution - use 1 to do SEQUENTIALLY, better for debugging
    n_par_files = 100
    for chunk in [files[i:i+n_par_files] for i in range(0, len(files), n_par_files) ]:
        with get_context("fork").Pool(processes=None) as pool:  # Adjust number of processes as needed
            #break
            pool.map(process_file, chunk)


