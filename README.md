# PoPS-Global_HPC
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Pandemic_model: HPC-ready

This is a version of the [Pandemic model](https://github.com/ncsu-landscape-dynamics/Pandemic_Model) set up to run on NCSU's HPC, henry2. The key differences are:

1. All paths are relative to the parent directory.
2. The model script is run from command line with five additional arguments: alpha, lamda, start year, start run (ie. 0), end run (eg. 49).
3. Parallel processing with multiprocess and subprocess is limited by setting the Pool to 1. Multiple commands are instead submitted using [pynodelauncher](https://github.com/ncsu-landscape-dynamics/pynodelauncher), a Python adaptation of [launch](https://github.ncsu.edu/lllowe/launch), which administers the tasks in parallel across the cores requested from HPC.
This, 
    1. allows for the use of distributed (vs. shared) memory, and 
    2. prevents the model from spawning additional threads that could affect the performance of other jobs on shared nodes.
4. The commands are written to a text file, which is submitted with pynodelauncher from an LSF batch script. See the [tutorials](https://projects.ncsu.edu/hpc/Documents/LSF.php) for more information on how to use henry2. 

### How to use:

Clone this repository to HPC (recommended: to /share/$GROUP/$USER)

```
git clone https://github.com/ncsu-landscape-dynamics/pandemic_hpc
cd pandemic_hpc
```
Run the [Pandemic Data Acquisition notebook](https://github.com/ncsu-landscape-dynamics/Pandemic_Model/blob/master/notebooks/1_data_acquisition_format.ipynb) locally and copy to the "inputs" directory.

So that you don't need to edit file names within the scripts, name input files as follows:
 - countries.gpkg
 - climate_similarities.npy
 - distance_matrix.npy
 - first_records_validation.csv

Use nano to modify model parameters in 'global_config.py'. 
```
nano global_config.py
```

To set up the environment and write the commands that will be run, submit (1) hpc/create_env_file.py, (2) global_config.py, and (3) hpc/command_writer.py with a short LSF batch script (e.g. submit_setup.csh).

```
bsub < submit_setup.csh 
```

Modify or copy 'submit_launch.csh' to adjust the resources requested (especially -n and -W). If you are in the landscape-dynamics lab group, the conda environment has already been created on HPC and is referenced in 'submit_launch.csh'. If you are not, the conda commands to set it up are included below.

Submit the script.

Once your job is complete, if it finished without error, you can calculate the summary statistics. If the job was cut short by the time limit, you may need to resume runs. To check which runs were completed and write out commands for missing runs, adjust and submit 'submit_check.csh', which will run 'run_checker,py'. 

If there are pending runs, modify 'submit_launch.csh' to replace commands.txt with the new text file, 'pending_runs.txt', and the remaining resources needed.

Once all the runs are completed, adjust and submit 'submit_summary.csh'. This script requests exclusive use of a single node to run in parallel with multiprocess using shared memory. 

### Setting up the Pandemic conda environment:

```
module load conda
conda create --prefix /path/to/env/env_pandemic Fiona=1.8.13 Rtree=0.9.4 argparse=1.4.0 attrs=19.3.0 certifi=2020.4.5.1 chardet=3.0.4 click-plugins=1.1.1 click=7.1.2 cligj=0.5.0 cycler=0.10.0 decorator=4.4.2 enum34=1.1.10 gdal=3.0.4 geographiclib=1.50 geopandas=0.7.0 geopy=1.22.0 idna=2.9 kiwisolver=1.2.0 matplotlib=3.2.1 munch networkx=2.4 numpy pandas=1.0.4 psycopg2=2.8.5 pydot=1.4.1 pyparsing pyproj=2.6.1.post1 python-dateutil=2.8.1 pytz=2020.1 requests=2.23.0 scipy shapely=1.7.0 six=1.15.0 urllib3=1.25.9 python-dotenv

```
To install pynodelauncher:
```
conda activate /path/to/env/env_pandemic
module load PrgEnv-intel
pip install git+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
conda deactivate
```

### Contents

- "pandemic" directory: Pandemic model scripts with limited modification
- "hpc" directory: scripts specific to running the model on HPC
- "inputs" directory: where all input data needs to be provided to the model
- "outputs" directory: where all model outputs and summary statistics will go
- files in main directory: global_config.py to provide study parameters, LSF batch scripts to submit various tasks
