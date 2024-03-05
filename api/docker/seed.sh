#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate raw
python -m raw.engine create --data_path data/
