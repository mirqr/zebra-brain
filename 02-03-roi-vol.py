# ruff: noqa: F403 F405 F401
import os
import re
import glob
import subprocess
import pandas as pd
import numpy as np

import subprocess
from multiprocessing import Pool
from multiprocessing import get_context # for macos


from utils_general import *
from utils_reg import *
from utils_stat import *


def make_folder(folder):
    """Create a folder if it does not exist and return its path."""
    os.makedirs(folder, exist_ok=True)
    return folder

def check_aux_files():
    for region in [4, 8, 149]:
        atlas_roi = f"aux/02-roi/Zbrain_atlas_{region}region.nii.gz"
        atlas_roi_head = f"aux/02-roi/roi_{region}region_header.csv"
        check_files(atlas_roi)
        check_files(atlas_roi_head)

    print()
    for region in [4, 8]:
        atlas_vol = f"aux/03-vol/Zbrain_atlas_{region}region_rsp.nii.gz"
        atlas_vol_head = f"aux/03-vol/vol_{region}region_header.csv"
        
        check_files(atlas_vol)
        check_files(atlas_vol_head)


def process_roi(divided_c0_file):
    #print (divided_c0_file)
    #return
    for region in [4, 8, 149]:
        zbrain_file_atlas_r = f"aux/02-roi/Zbrain_atlas_{region}region.nii.gz" 
        
        divided_c0_base = os.path.basename(divided_c0_file).replace("r_", "")
        
        roi_folder = f"{experiment_folder}/roi_{region}region/C0divC1"
        file_out = divided_c0_base.replace(".nii.gz", f"_{region}_roi.csv")
        file_output = f"{roi_folder}/{file_out}"

        values = compute_roi(divided_c0_file, zbrain_file_atlas_r, file_output)
        
        # rewrite but append the input file
        with open(file_output, 'w') as f:
            base_name = divided_c0_base.replace("_C0divC1.nii.gz", "")
            f.write(f"{base_name}, {values}")
        #os.remove(file_output)
        print(values)

def process_vol(mask_file):
    for region in [4, 8]:
        zbrain_file_atlas_v = f"aux/03-vol/Zbrain_atlas_{region}region_rsp.nii.gz"
        
        mask_file_name = os.path.basename(mask_file).replace("mask_ja_", "")
        
        vol_folder = f"{experiment_folder}/vol_{region}region" # no /C0divC1
        file_out = mask_file_name.replace(".nii.gz", f"_{region}_vol.csv")
        file_output = f"{vol_folder}/{file_out}"

        values = compute_roi(mask_file, zbrain_file_atlas_v, file_output)
        with open(file_output, 'w') as f:
            base_name = mask_file_name.replace(".nii.gz", "")
            f.write(f"{base_name}, {values}")
        #os.remove(file_output)
        print(values)

def concat_my(df, region, kind='roi'):
    if kind == 'roi':
        header = pd.read_csv(f"aux/02-roi/roi_{region}region_header_my.csv")
    if kind == 'vol':
        header = pd.read_csv(f"aux/03-vol/vol_{region}region_header_my.csv")
    # add the header to df
    df.columns = header.columns # put same columns
    return df

def write_table(df, region, kind='roi'):
    if kind=='roi':
        file_out = f"{experiment_folder}/ALL_roi_{region}_region"
        header = pd.read_csv(f"aux/02-roi/roi_{region}region_header.csv",  header=None)
    elif kind=='vol':
        file_out = f"{experiment_folder}/ALL_vol_{region}_region"
        header = pd.read_csv(f"aux/03-vol/vol_{region}region_header.csv",  header=None)
    else:
        raise ValueError('kind must be roi or vol')
    
    df.columns = header.columns # put same columns
    df_concat = pd.concat([header, df], ignore_index=True)
    # assert size
    assert df_concat.shape[1] == region+1 # plus the name  # assert 150 columns

    # add csv
    df_concat.to_csv(f"{file_out}.csv", index=False, header=False)
    # add xlsx
    df_concat.to_excel(f"{file_out}.xlsx", index=False, header=False)



if __name__ == "__main__":

    # INPUT
    experiment_folder = 'data/data_dyrka'
    #

    check_aux_files()

    input_pattern_div = f"{experiment_folder}/divided/C0divC1/*.nii.gz"
    check_files(input_pattern_div)
    input_pattern_ja = f"{experiment_folder}/jacobian/mask_ja_*.nii.gz"
    check_files(input_pattern_ja)

    # create the folders
    for region in [4, 8, 149]:
        make_folder(f"{experiment_folder}/roi_{region}region/C0divC1")
    for region in [4, 8]:
        make_folder(f"{experiment_folder}/vol_{region}region")
        
    proc = 1 # sequentially (process only uses one core)
    proc = None # use all available cores.
    # parallel
    with get_context("fork").Pool(processes=proc) as pool:  # Adjust number of processes as needed
        pass
        pool.map(process_roi, sorted(glob.glob(input_pattern_div)))
        pool.map(process_vol, sorted(glob.glob(input_pattern_ja)))


    # concat all roi and vol files - create combined file
    dict_df_roi = {}
    for region in [4, 8, 149]:
    #for region in [4, 8,]:
        roi_folder = f"{experiment_folder}/roi_{region}region/C0divC1"
        df_temp = pd.concat([pd.read_csv(f, header=None) for f in sorted(glob.glob(f"{roi_folder}/*.csv"))], ignore_index=True).copy()
        if region == 149: # remove all 0 columns
            df_temp = df_temp.loc[:, (df_temp != 0).any(axis=0)]
            assert df_temp.shape[1] == 149+1 # plus the name  # assert 150 columns
        write_table(df_temp, region, kind='roi')
        

    dict_df_vol = {}
    for region in [4, 8]:
        #break
        vol_folder = f"{experiment_folder}/vol_{region}region"
        df_temp = pd.concat([pd.read_csv(f, header=None) for f in sorted(glob.glob(f"{vol_folder}/*.csv"))], ignore_index=True).copy()
        write_table(df_temp, region, kind='vol')
        






