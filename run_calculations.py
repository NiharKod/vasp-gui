import os
import subprocess
import resource

class Calculations:
    def __init__(self, incar, potcar, poscar, allocation_type, queue_partition, num_nodes, num_tasks, time_requested):
        self.incar = incar
        self.potcar = potcar
        self.poscar = poscar
        
        self.allocation_type = allocation_type
        self.queue_partition = queue_partition
        self.num_nodes = num_nodes
        self.num_tasks = num_tasks
        self.time_requested = time_requested
        
        self.output_directory = os.path.expanduser("~/Desktop/vasp_output/")
        self.job_script_path = os.path.expanduser("~/Desktop/vasp_job_script.sh")
        
        

    def call_calculations(self):
        """Run the VASP calculations using srun."""
        try:
            # Set unlimited memory
            set_unlimited_memory()

            # Ensure the output directory exists
            os.makedirs(self.output_directory, exist_ok=True)

            # Copy input files to the output directory
            subprocess.run(
                f"cp {self.incar} {self.potcar} {self.poscar} {self.output_directory}",
                shell=True,
                check=True
            )

            # Write the job script to a file that will be executed by srun
            with open(self.job_script_path, "w") as job_script:
                job_script.write(f"""#!/bin/bash
                                 
#SBATCH -A {self.allocation_type}  # Allocation name
#SBATCH --nodes={self.num_nodes}     # Total # of nodes 
#SBATCH --ntasks={self.num_tasks}    # Total # of MPI tasks
#SBATCH --time=00:30:00   # Total run time limit (hh:mm:ss)
#SBATCH -J testvaspjob  # Job name
#SBATCH -o testvaspjob.o  # Name of stdout output file
#SBATCH -e testvaspjob.e  # Name of stderr error file
#SBATCH -p wholenode   # Queue (partition) name

# Load necessary modules
module load gcc/11.2.0 openmpi/4.1.6
module load vasp/6.3.0

# Change to the output directory
cd {self.output_directory}

# Run the VASP calculation
mpirun -np 256 vasp_std
""")

            # Make the job script executable
            subprocess.run(f"chmod +x {self.job_script_path}", shell=True, check=True)

            # Run the job script using srun
            command = f"sbatch {self.job_script_path}"
            subprocess.run(command, shell=True, check=True)

            print("VASP calculations completed successfully!")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            print(f"Error details: {e.stderr}")

def set_unlimited_memory():
    """Set the locked memory limit to unlimited."""
    soft, hard = resource.getrlimit(resource.RLIMIT_MEMLOCK)
    resource.setrlimit(resource.RLIMIT_MEMLOCK, (hard, hard))
    print(f"Updated RLIMIT_MEMLOCK: Soft = {hard}, Hard = {hard}")
