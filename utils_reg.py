import os
import subprocess
import nibabel as nib
import numpy as np

#import ants
   

def preprocess(input_path, output_path):
    """Converts .nrrd to .nii.gz using BisWeb preprocessoptical."""
    if os.path.isfile(output_path):
        print(f"Skipping preprocessing for {output_path}, already exists")
        return 

    command = f"biswebnode preprocessoptical --ras --biascorrect false --mask false --normalize false --resample --factor 1 --sigma 1 -i {input_path} --output {output_path}"
    run_command(command)

def nonlinear_registration(input_file, non_param_file, standard_reference, output_xform):
    """Runs BisWeb non-linear registration."""
    if os.path.isfile(output_xform):
        print(f"--!!!!!! Skipping registration for {output_xform}, already exists")
        return
    
    command = f"biswebnode nonlinearregistration --paramfile {non_param_file} -r {standard_reference} -t {input_file} -o {output_xform}"

    # append file name to the command
    command = add_timing(command, output_file_path=output_xform)
    
    run_command(command)


def reslice_image(input_file, reference_file, transform_file, output_file):
    """Runs BisWeb reslicing."""
    if os.path.isfile(output_file):
        print(f"Skipping reslicing for {output_file}, already exists")
        return

    command = f"biswebnode resliceImage -r {reference_file} -i {input_file} -x {transform_file} -o {output_file}"
    run_command(command)

# not working. cant read the transform file generated by bisweb
#def reslice_image_new2(input_file, reference_file, transform_file, output_file):
#    """Apply transformation to reslice an image"""
#    print(f"Reslicing {input_file} to {output_file}")
#    fixed = ants.image_read(reference_file)
#    moving = ants.image_read(input_file)
#
#    resliced_img = ants.apply_transforms(fixed, moving, transformlist=[transform_file])
#    ants.image_write(resliced_img, output_file)


def divide_images(nifti1, nifti2, output_file):
    """Runs FSL division."""
    command = f"fslmaths {nifti1} -div {nifti2} {output_file}"
    run_command(command)

def divide_images_new(nifti1, nifti2, output_file):
    """Divide two images and save the result"""
    print(f"Dividing {nifti1} by {nifti2} and saving to {output_file}")
    img1 = nib.load(nifti1).get_fdata()
    img2 = nib.load(nifti2).get_fdata()

    divided = np.divide(img1, img2, where=(img2 != 0))  # Avoid division by zero. Result is 0 where img2 is 0
    nifti_img = nib.Nifti1Image(divided, nib.load(nifti1).affine)
    nib.save(nifti_img, output_file)


def compute_jacobian(transform_file, image, output_jacobian):
    """Computes Jacobian determinant using BisWeb."""
    if os.path.isfile(output_jacobian):
        print(f"Skipping Jacobian computation for {output_jacobian}, already exists")
        return

    command = f"biswebnode jacobianimage -x {transform_file} -i {image} -o {output_jacobian}"
    run_command(command)


def apply_mask(image_file, mask_file, output_file):
    """Applies a mask using BisWeb."""
    if os.path.isfile(output_file):
        print(f"Skipping mask application for {output_file}, already exists")
        return
    
    command = f"biswebnode maskimage -i {image_file} -m {mask_file} -o {output_file}"
    run_command(command)


def compute_roi(input_file, zbrain_file_atlas, output_file):
    command = f"biswebnode computeroi -i {input_file} -r {zbrain_file_atlas} -o {output_file}"
    run_command(command)
    # read the file - is just one line
    with open(output_file, 'r') as f:
        roi = f.readline()
    return roi


def run_command(command):
    """Executes a shell command."""
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)



def add_timing(command, output_file_path = None): # add other usefull parameters
    """Adds GNU time command to a shell command."""
    # # python subprocess.run() likely capturing the output from the GNU time utility (usually /usr/bin/time), not shell built-in time 
    output_file = os.path.basename(output_file_path) 
    output_folder = os.path.dirname(output_file_path)

    time_format = f"'{output_file}: %e real; %U user; %S sys'"
    # carefull with > and >> (overwrite or append)
    command_with_time = f"time -f {time_format} {command} 2>> {output_folder}/time.log"
    # both the command's output and the timing information
    #command_with_time = f"time -f {time_format} {command} > command_output.log 2> time.log" 
    # everything in the same file
    #command_with_time = f"time -f {time_format} {command} > command_output.log 2>&1" 
    return command_with_time