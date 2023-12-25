# Improvement

- Our method introduces a improvement by leveraging a continuous representation achieved through the integration of a hash grid, codebook, and neural network. This innovative approach aims to minimize storage requirements while simultaneously enhancing rendering speed.
- Applying a novel volume-based masking strategy that identifies and removes non-essential Gaussians. This aims to reduce the number of Gaussians and improve runtime efficiency.
- Each Gaussian in 3D Gaussian Splatting requires 48 of the total 59 parameters to represent different colors according to the viewing direction. Instead of using the naive and parameter-inefficient approach, we represent the view-dependent color of each Gaussian by exploiting a grid-based neural field. To this end, we exploit hash grids followed by a tiny MLP to represent color. Here, we input positions into the hash grids, and then the resulting feature and the view direction are fed into the MLP. The result will be used to be converted into RGB colors
- Previous method represents a scene with numerous small Gaussians collectively, and each Gaussian primitive is not expected to show high diversity. In this improvement, we use a codebook-based approach for modeling the geometry of Gaussians. It learns to find similar patterns or geometry shared across each scene and only stores the codebook index for each Gaussian, which helps to reduce spatial and computational resources
# NeRF Synthetic
### Result
|           | SSIM | PSNR | LPIPS |
| --------- | ---- | ---- | ----- |
| lego      |      |      |       |
| mic       |      |      |       |
| ficus     |      |      |       |
| chair     |      |      |       |
| hotdog    |      |      |       |
| ship      |      |      |       |
| materials |      |      |       |
| drums     |      |      |       | 
### Visualize
|          | Render Image    | Grouth truth     | 
| -------- | ------- | -------- |
| lego     | ![[Images/nerf/lego.png]] | ![[Images/nerf/lego_gt.png]] |
| mic      | ![[Images/nerf/mic.png]] | ![[Images/nerf/mic_gt.png]] |
| ficus    | ![[Images/nerf/ficus.png]] | ![[Images/nerf/ficus_gt.png]] |
| chair    | ![[Images/nerf/chair.png]] | ![[Images/nerf/chair_gt.png]] |
| hotdog   | ![[Images/nerf/hotdog.png]] | ![[Images/nerf/hotdog_gt.png]] |
| ship     | ![[Images/nerf/ship.png]] | ![[Images/nerf/ship_gt.png]] |
| materials| ![[Images/nerf/materials.png]] | ![[Images/nerf/materials_gt.png]] |
| drums    | ![[Images/nerf/drums.png]] | ![[Images/nerf/drums_gt.png]] |
# MipNeRF 360
### Result
|         | SSIM | PSNR | LPIPS |
| ------- | ---- | ---- | ----- |
| bicycle |      |      |       |
| bonsai  |      |      |       |
| counter |      |      |       |
| garden  |      |      |       |
| kitchen |      |      |       |
| stump   |      |      |       |
| room    |      |      |       | 

### Visualize
|          | Render Image    | Grouth truth     | 
| -------- | ------- | -------- |
| bicycle  | ![[Images/mipnerf360/bicycle.png]] | ![[Images/mipnerf360/bicycle_gt.png]] |
| bonsai   | ![[Images/mipnerf360/bonsai.png]] | ![[Images/mipnerf360/bonsai_gt.png]] |
| counter  | ![[Images/mipnerf360/counter.png]] | ![[Images/mipnerf360/counter_gt.png]] |
| garden   | ![[Images/mipnerf360/garden.png]] | ![[Images/mipnerf360/garden_gt.png]] |
| kitchen  | ![[Images/mipnerf360/kitchen.png]] | ![[Images/mipnerf360/kitchen_gt.png]] |
| stump    | ![[Images/mipnerf360/stump.png]] | ![[Images/mipnerf360/stump_gt.png]] |
| room     | ![[Images/mipnerf360/room.png]] | ![[Images/mipnerf360/room_gt.png]] |
# Tank&Temple
### Result (New)

|       | SSIM  | PSNR   | LPIPS |
| ----- | ----- | ------ | ----- |
| truck | 0.870 | 24.54  | 0.159 |
| train | 0.796 | 21.263 | 0.233 | 

### Comparison

|                            | truck | train  |
| -------------------------- | ----- | ------ |
| Vanilla gaussian splatting | 24.08 | 19.65  |
| Ours                       | 24.54 | 21.263 |
### Visualize
|          | Render Image    | Grouth truth     | 
| -------- | ------- | -------- |
| truck  | ![[truck_3dgs.png]] | ![[Images/tank&temple/truck_gt.png]] |
| train   | ![[train_3dgs.png]] | ![[Images/tank&temple/train_gt.png]] |

# LLFF Dataset

### Result

|          | SSIM  | PSNR   | LPIPS |
| -------- | ----- | ------ | ----- |
| fern     | 0.808 | 23.897 | 0.214 |
| flower   | 0.844 | 27.058 | 0.214 |
| fortress | 0.882 | 29.848 | 0.178 |
| horns    | 0.878 | 26.551 | 0.190 |
| orchids  | 0.656 | 19.614 | 0.246 |
| room     | 0.945 | 30.041 | 0.142 |
| trex     | 0.902 | 25.441 | 0.189 |

### Comparison


|                            | fern   | flower | fortress | horns  | orchids | room   | trex   |
| -------------------------- | ------ | ------ | -------- | ------ | ------- | ------ | ------ |
| Vanilla gaussian splatting | 23.897 | 27.145 | 29.856   | 27.129 | 19.728  | 31.593 | 25.45  |
| Ours                       | 23.897 | 27.058 | 29.848   | 26.551 | 19.614  | 30.041 | 25.441 |

### Visualize

|          | Render Image                      | Ground truth                         |
| -------- | --------------------------------- | ------------------------------------ |
| fern     | ![[fern_3dgs.png]]                     | ![[fern_gt.png]]                     |
| flower   | ![[flower_3dgs.png]]                   | ![[flower_gt.png]]                   |
| fortress | ![[fortress_3dgs.png]]                 | ![[fortress_gt.png]]                 |
| horns    | ![[horns_3dgs.png]]                    | ![[horns_gt.png]]                    |
| orchids  | ![[orchids_3dgs.png]]                  | ![[orchids_gt.png]]                  |
| room     | ![[room_3dgs.png]] | ![[Images/llff dataset/room_gt.png]] |
| trex     | ![[trex_3dgs.png]]                     | ![[trex_gt.png]]                     | 

