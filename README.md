# **BREEZE-Mapping Pipeline: a Standalone Python Implementation**  

## **Overview**  
This repository provides an improved and fully portable implementation of the **BREEZE-mapping pipeline** for whole-brain structural and activity analysis in larval zebrafish, introduced in:

**Jin, Neelakantan, et al.** (2023) – *Brain Registration and Evaluation for Zebrafish (BREEZE)-mapping: A pipeline for whole-brain structural and activity analyses.* [STAR Protocols, DOI: 10.1016/j.xpro.2023.102647](https://doi.org/10.1016/j.xpro.2023.102647)  

The original pipeline is designed for HPC infrastructure with Slurm workload management and relies on root access and multiple external dependencies, including proprietary software.

This repository provides a standalone Python implementation that can be run on a wider range of machine with minimal setup requirements.


## Key Improvements

- Replaced Bash scripts with Python for better readability, maintainability
- Simplified and isolated setup in a Conda environment. No Root Required. Removed unnecessary (proprietary) dependencies (e.g., MATLAB)
- Optimized parallelization by identifying only the necessary parts that require parallel execution, using Python subprocesses instead of Slurm
- Improved portability - can run on standard laptops to high-performance workstations

For information, contact: 
- Mirko Nardi (Postdoctoral Researcher, Computer Science Dept., Scuola Normale Superiore - IIT-CNR) - mirko.nardi@sns.it 
- Matteo DiGregorio (PhD candidate, Biology Dept., University of Pisa) - matteo.digregorio@unipi.it
