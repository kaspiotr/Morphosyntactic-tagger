#!/bin/bash -l

module load plgrid/apps/cuda/10.0
module load plgrid/tools/python/3.6.5

source prometheus_venv/bin/activate

export LD_LIBRARY_PATH=/net/scratch/people/plgkaspiotr/cuda/lib64:$LD_LIBRARY_PATH
export LIBRARY_PATH=/net/scratch/people/plgkaspiotr/cuda/lib64:$LIBRARY_PATH
export CPATH=/net/scratch/people/plgkaspiotr/cuda/include:$CPATH

echo {1..10} | xargs -t -P 10 -n 1 srun -n 1 -N 1 --ntasks-per-node=1 -A lemkingpu2 --partition=plgrid-gpu --gres=gpu:1 --mem-per-cpu=64GB --time=72:00:00 --mail-type=ALL --mail-user=kaspiotr@gmail.com python3 training_experiment_2.py


