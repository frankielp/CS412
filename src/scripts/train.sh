#!/bin/bash
cd ..
DATASETS=("mic" "ficus" "chair" "hotdog" "materials" "drums" "ship")
# DATASETS=("counter" "garden" "kitchen" "stump")
unset CUDA_VISIBLE_DEVICES
for dataset in "${DATASETS[@]}"; do
    python train.py -s dataset/nerf_synthetic/${dataset} --eval -m output/${dataset} &
    echo "Launched ${dataset}"
wait
done