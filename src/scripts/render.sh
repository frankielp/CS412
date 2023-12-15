#!/bin/bash
cd ..
# unset CUDA_VISIBLE_DEVICES
export CUDA_VISIBLE_DEVICES=1
# MIPNERF=("garden" "stump" "bonsai" "room")
# for dataset in "${MIPNERF[@]}"; do
#     python render.py -m output/mipnerf360_${dataset}/ --iteration 30000
# wait
# done
# "mic" "ficus" "chair" "hotdog" "materials" "drums" "ship"
# "counter" "garden" "kitchen"
NERF=("materials" "drums" "ship")
for dataset in "${NERF[@]}"; do
    python render.py -m output/${dataset}/ --iteration 30000 
wait
done