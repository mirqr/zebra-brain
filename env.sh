#!/bin/bash

conda create -n zebra2 python=3.10 -y
conda activate zebra2
conda install nodejs -y

npm install -g biswebnode@1.3.0 mocha@11.1.0 

conda install -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public/  -c conda-forgey fsl-avwutils -y
conda install hcc::afni jpeg  -y

pip install -r requirements.txt

# use 
# source env.sh . env.sh 
