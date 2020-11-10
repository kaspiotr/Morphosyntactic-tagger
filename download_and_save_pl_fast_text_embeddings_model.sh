#!/bin/bash

module load plgrid/tools/python/3.6.5

source prometheus_venv/bin/activate

python3 download_and_save_pl_fast_text_embeddings_model.py