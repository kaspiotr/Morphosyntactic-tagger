#!/bin/bash

module load plgrid/tools/python/3.6.5

source prometheus_venv/bin/activate

python3 create_and_save_polish_letters_dictionary.py