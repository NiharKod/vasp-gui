# VASP GUI for Anvil Supercomputer

## Overview

This project provides a Graphical User Interface (GUI) for running VASP (Vienna Ab initio Simulation Package) jobs on the Anvil Supercomputer. Built using Python, the GUI streamlines the process of setting up and managing VASP calculations by automating job submission, file uploads, and execution on the Anvil cluster.

## Features

### Job Submission
- Configure and initiate VASP jobs on Anvil by specifying:
  - Partition
  - Number of cores/nodes
  - Wall time
  - Additional SLURM parameters

### VASP Input File Management
- Upload essential VASP input files directly through the GUI:
  - POSCAR
  - INCAR
  - POTCAR
  - KPOINTS

### Calculation Execution
- Seamlessly run VASP calculations after uploading input files and configuring job parameters.

## Prerequisites

- Python (version 3.8 or higher)
- Required Python libraries (install via pip) - PyQT5
- Access to the Anvil Supercomputer with SSH credentials



