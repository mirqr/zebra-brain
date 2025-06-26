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
- Improved portability - runs seamlessly on standard laptops as well as high-performance workstations.


For information, contact: 
- Mirko Nardi (Postdoctoral Researcher, Computer Science Dept., Scuola Normale Superiore - IIT-CNR) - mirko.nardi@sns.it 
- Matteo DiGregorio (PhD candidate, Biology Dept., University of Pisa) - matteo.digregorio@unipi.it
