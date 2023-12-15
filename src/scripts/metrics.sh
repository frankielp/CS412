#!/bin/bash
cd ..
DATASETS=("mipnerf360_bicycle" "ship")
# DATASETS=("counter" "garden" "kitchen" "stump")
export CUDA_VISIBLE_DEVICES=2
for dataset in "${DATASETS[@]}"; do
    python metrics.py -m output/${dataset} &
    echo "Launched ${dataset}"
wait
done