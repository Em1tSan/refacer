#!/bin/bash
git pull

python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -U setuptools
python3 -m pip install -r requirements.txt

echo Opening Refacer...

export PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:512
export CUDA_MODULE_LOADING=LAZY

source venv/bin/activate

python3 app.py --gpu-threads 4 --max-memory 16000 --autolaunch --video_quality 18 --frame_limit 1000
