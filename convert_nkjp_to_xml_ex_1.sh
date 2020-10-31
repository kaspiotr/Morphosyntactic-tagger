#!/bin/bash

module load plgrid/tools/python/3.6.5

source prometheus_venv/bin/activate

python3 convert_nkjp_to_xml.py