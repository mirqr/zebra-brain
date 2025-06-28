# **BREEZE-Mapping Pipeline: a Standalone Python Implementation**  

## **Overview**  
This repository provides an improved and fully portable implementation of the **BREEZE-mapping pipeline** for whole-brain structural and activity analysis in larval zebrafish, introduced in:

**Jin, Neelakantan, et al.** (2023) – *Brain Registration and Evaluation for Zebrafish (BREEZE)-mapping: A pipeline for whole-brain structural and activity analyses.* [STAR Protocols, DOI: 10.1016/j.xpro.2023.102647](https://doi.org/10.1016/j.xpro.2023.102647)  

The original pipeline is designed for HPC infrastructure with Slurm workload management and relies on root access and multiple external dependencies, including proprietary software.

This repository provides a standalone Python implementation that can be run on a wider range of machine with minimal setup requirements.


## Key Improvements

- Migrated from Bash to Python for improved readability and maintainability
- Streamlined and modularized setup using a Conda environment — no root access required
- Eliminated unnecessary and proprietary dependencies (e.g., MATLAB) to simplify deployment
- Optimized parallel execution by isolating performance-critical sections and leveraging Python’s subprocess module instead of relying on Slurm
- Improved portability - runs seamlessly on standard laptops as well as high-performance workstations


For information, contact: 
- Mirko Nardi (Postdoctoral Researcher, Computer Science Dept., Scuola Normale Superiore - IIT-CNR) - mirko.nardi@sns.it 
- Matteo DiGregorio (PhD candidate, Biology Dept., University of Pisa) - matteo.digregorio@unipi.it


# Installation

## Prerequisites


This pipeline has been tested on **Linux** systems.
**Note**: The `afni` package is only available on **Linux** or **Windows Subsystem for Linux (WSL)**. 


- [Conda](https://github.com/conda-forge/miniforge) Miniforge is recommended for a lightweight Conda installation.



## Installation Steps

1. Clone the repository and navigate into the project directory:

   ```bash
   git clone <your-repo-url>
   cd zebra-brain
   ```

2. Initialize the Conda environment:

   ```bash
   source env.sh
   ```

This will create and activate an isolated environment named `zebra-env` with all the required dependencies. 

## Configuration

Before running the pipeline, configure the working directory:

- Open each `.py` script and set the `experiment_folder` variable to the path where your input data is located.


## Running the Pipeline

To run individual steps of the pipeline, activate the environment and execute the relevant scripts:

```bash
conda activate zebra-env  # Activate the environment

# Run the registration step
python 01-reg.py  

# Run the ROI volume step
python 02-03-roi-vol.py  
```
