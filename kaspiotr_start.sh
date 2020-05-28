#!/bin/bash -l
## Liczba alokowanych węzłów
#SBATCH -N 1
## Liczba zadań per węzeł (domyślnie jest to liczba alokowanych rdzeni na węźle)
#SBATCH --ntasks-per-node=1
## Ilość pamięci przypadającej na jeden rdzeń obliczeniowy (domyślnie 5GB na rdzeń)
#SBATCH --mem-per-cpu=48GB
## Maksymalny czas trwania zlecenia (format HH:MM:SS)
#SBATCH --time=00:01:00
## Nazwa grantu do rozliczenia zużycia zasobów
#SBATCH -A lemkingpu2
## Zlecenie zadan odbywa sie poprzez podanie ponizszych dwoch opcji systemu kolejkowego
#SBATCH --partition=plgrid-gpu-v100
## --gres=gpu[:count] w przypadku gdy nie ma podanej opcji count, system kolejkowy i tak domyslnie alokuje jedna karte na wezle obliczeniowym
## Po zleceniu zadania system kolejkowy automatycznie ustawia zmienna srodowiskowa $CUDA_VISIBLE_DEVICES oraz zezwala na dostep do zaalokowanych do kart.
#SBATCH --gres=gpu:1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=kaspiotr@gmail.com

module load plgrid/apps/cuda/10.1
module load plgrid/tools/python/3.6.5

source /net/scratch/people/plgkaspiotr/morphosyntactic-tagger/prometheus_venv/bin/activate

export LD_LIBRARY_PATH=/net/scratch/people/plgkaspiotr/cuda/lib64:$LD_LIBRARY_PATH
export LIBRARY_PATH=/net/scratch/people/plgkaspiotr/cuda/lib64:$LIBRARY_PATH
export CPATH=/net/scratch/people/plgkaspiotr/cuda/include:$CPATH

echo {1..10} | xargs -t -P 10 -n 1 srun -n 1 -N 1 --mem=6gb python3 training.py

