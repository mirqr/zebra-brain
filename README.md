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


# Installation and Usage Instructions

This repository is designed to be run in a Conda environment, which allows for easy management of dependencies and isolation of the Python environment.

This pipeline has been tested on **Linux**. Steps 1-4 can run on any platform with a properly installed Conda environment. However, Steps 5+ require Linux (including Windows Subsystem for Linux (WSL)) due to the ``afni`` package dependency, which is Linux-exclusive.


## Prerequisites

- [Conda](https://github.com/conda-forge/miniforge) Miniforge is recommended for a lightweight Conda installation.


## Installation Steps

1. Clone/download the repository
2. Navigate into the project directory and initialize the Conda environment:

   ```bash
   cd zebra-brain
   source env.sh
   ```

This will create and activate an isolated environment named `zebra-env` with all the required dependencies, including a `nodejs` installation required for `BioImage Suite Web` tool.

## Experimental Configuration

Each step of the pipeline expects an input folder containing the images to be processed.

Following the structure of the original BREEZE-mapping pipeline, place the images for Step 1 (registration) into:

```
data/<your_experiment>/nrrd/
```

Before running the pipeline, configure the working directory:

- Open each `.py` script and set the `experiment_folder` variable to the path of your experiment folder, e.g., `data/<your_experiment>`.


## Running the Pipeline

To run individual steps of the pipeline, activate the environment and execute the relevant scripts:

```bash
conda activate zebra-env  # Activate the environment

# Run the registration step
python 01-reg.py  
```

Once the registration step is complete, you can proceed with the next steps in the pipeline:

```bash
# Run the ROI volume step
python 02-03-roi-vol.py  
```

To be continued...