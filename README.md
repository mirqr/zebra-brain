# **BREEZE-Mapping Pipeline: a Standalone Python Implementation**  

## **Overview**  
This repository provides an improved and fully portable implementation of the **BREEZE-mapping pipeline** for whole-brain structural and activity analysis in larval zebrafish, based on:

**Jin, Neelakantan, et al.** (2023) – *Brain Registration and Evaluation for Zebrafish (BREEZE)-mapping: A pipeline for whole-brain structural and activity analyses.* [STAR Protocols, DOI: 10.1016/j.xpro.2023.102647](https://doi.org/10.1016/j.xpro.2023.102647)  

The original pipeline assumes access to high-performance computing (HPC) infrastructure with Slurm workload management, requiring proprietary (MATLAB) or root-level permissions to install dependencies.

This Python implementation replaces the original Bash version with a lightweight, self-contained solution that eliminates unnecessary dependencies and parallelization overhead. The result is a portable tool that runs efficiently on any machine, from servers to standard laptops.

## Key Improvements


- **Pure Python Implementation** – Replaced Bash scripts with Python for better readability, maintainability, and portability.  
- **Simplified and Isolated Setup** - Single-command installation in an isolated Conda environment, avoiding software conflicts. **No Root** Access Required. **No proprietary dependencies** (e.g. MATLAB), replacing them with **equivalent Python code**.  
- **Optimized Parallelization** – Identified **only the necessary parts** that require parallel execution, using Python subprocesses instead of Slurm.  
- **Better Portability** – Runs on standard laptops to high-performance workstations
