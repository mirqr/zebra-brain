import glob
import os

import nibabel as nib  # get_fdata() to LOAD THE ACTUAL DATA  (numpy array)
import numpy as np
import pandas as pd
from matplotlib.pyplot import plot

from utils_general import *


def compute_reference_mean_std(reference_list): 
    referenceImages = []
    for ref_file in reference_list:
        referenceImages.append(nib.load(ref_file).get_fdata())

    # Load all WT images into a NumPy array (stacked along a new axis)
    referenceImages = np.stack(referenceImages, axis=-1)  
    print(f"Stacked image shape: {referenceImages.shape}")  
    
    # Computes voxel-wise meand standard deviation efficiently. STD across the last axis (WT images)
    std_ref_img = np.std(referenceImages, axis=-1)  
    mean_ref_img = np.mean(referenceImages, axis=-1)

    # replace zero std values with small number 
    # Avoids NaN in division # TODO check if it's the best approach. not sure
    #std_ref_img[std_ref_img == 0] = 1e-6  
    
    return mean_ref_img, std_ref_img

def compute_save_comparison(comparison_list, mean_ref_img, std_ref_img, out_dir, reference_fish_image):
    ref_img = nib.load(reference_fish_image) # used once 
    for comparison_file in comparison_list:
        # Load the WT image
        comparison_img = nib.load(comparison_file).get_fdata() 

        # Compute voxel-wise Z-score
        #zscore_img = (comparison_img - mean_ref_img) / std_ref_img
        # use np division
        zscore_img = np.divide((comparison_img - mean_ref_img), std_ref_img, where=(std_ref_img != 0)) # avoid division by zero

        # Save Z-score image
        zscore_nifti = nib.Nifti1Image(zscore_img, affine=ref_img.affine) # affine (?) verify TODO 
        
        # get filename
        zscore_filename = os.path.basename(comparison_file).replace(".nii.gz", "_zscore.nii.gz")
        zscore_filename = f"{out_dir}/{zscore_filename}"
        nib.save(zscore_nifti, zscore_filename)
        print(f"Z-score normalized: {zscore_filename}")
        #return zscore_img



if __name__ == "__main__":

    # INPUT 
    control = "wt"; geno_types = ['het','hom']; experiment_folder = 'data/data_dyrka'
    #control = "A"; geno_types = ['B','C','D']; experiment_folder = ... # change as needed
    # INPUT 
    
    for geno_type in geno_types + [control]: # ensure control group is always checked (?)
        check_files(f"{experiment_folder}/divided/C0divC1/*_{geno_type}*C0divC1.nii.gz") # verifica hardcode su C0divC1

    # same aux file of reg
    reference_fish_image = "aux/01-reg/standard_ref.nii.gz"
    #DIV_TYPE_ls =["C0divC1","C2divC1"] # iterate over div types if needed
    div_type = "C0divC1" # we only have C0divC1 

    # prepare the output dir
    zscore_dir = f"{experiment_folder}/divided_zscore/{div_type}" # 
    os.makedirs(zscore_dir, exist_ok=True)

    control_files = glob.glob(f"{experiment_folder}/divided/{div_type}/r_*{control}*{div_type}.nii.gz")
    print(control_files) # poi lui scrive su file?? credo serva solo per passarlo a matlab
    print(f"Control group {control}: {len(control_files)}")

    mean_ref_img, std_ref_img = compute_reference_mean_std(reference_list = control_files)
    for geno_type in geno_types + [control]: 
        #pass
        comparison_group = glob.glob(f"{experiment_folder}/divided/{div_type}/r_*{geno_type}*{div_type}.nii.gz")
        print(f"Comparison group {geno_type}: {len(comparison_group)}")
        compute_save_comparison(comparison_group, mean_ref_img, std_ref_img, out_dir=zscore_dir, reference_fish_image = "aux/01-reg/standard_ref.nii.gz")


    #plot_nifti_slices(f"{experiment_folder}/divided_zscore/C0divC1/*.gz", layer_max=131, step=10, num_files_limit=200, cmap='gray')    
    #plot_nifti_slices(f"{experiment_folder}/divided_zscore/C0divC1/*.gz", layer_max=140, step=20, num_files_limit=100, cmap='gray')

    # Jacobian zscore
    # now is reference rsp 
    reference_fish_image = "aux/01-reg/standard_ref_rsp.nii.gz"

    zscore_jacob_dir = f"{experiment_folder}/jacobian_zscore" # 
    os.makedirs(zscore_jacob_dir, exist_ok=True)

    control_files = glob.glob(f"{experiment_folder}/jacobian/mask_ja_*{control}*.nii.gz")
    print(control_files)
    print(f"Control group {control}: {len(control_files)}")

    mean_ref_img, std_ref_img = compute_reference_mean_std(reference_list = control_files)
    for geno_type in geno_types + [control]:
        comparison_group = glob.glob(f"{experiment_folder}/jacobian/mask_ja*_{geno_type}*.nii.gz")
        print(f"Comparison group {geno_type}: {len(comparison_group)}")
        compute_save_comparison(comparison_group, mean_ref_img, std_ref_img, out_dir=zscore_jacob_dir, reference_fish_image = reference_fish_image)


    plot_nifti_slices(f"{zscore_dir}/*.gz", layer_max=131, step=10, num_files_limit=200, cmap='gray')

