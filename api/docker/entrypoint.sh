#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate raw
gunicorn -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker raw.main:app
