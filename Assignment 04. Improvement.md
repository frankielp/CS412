# Improvement

- Our method introduces a improvement by leveraging a continuous representation achieved through the integration of a hash grid, codebook, and neural network. This innovative approach aims to minimize storage requirements while simultaneously enhancing rendering speed.
- Applying a novel volume-based masking strategy that identifies and removes non-essential Gaussians. This aims to reduce the number of Gaussians and improve runtime efficiency.
- Each Gaussian in 3D Gaussian Splatting requires 48 of the total 59 parameters to represent different colors according to the viewing direction. Instead of using the naive and parameter-inefficient approach, we represent the view-dependent color of each Gaussian by exploiting a grid-based neural field. To this end, we exploit hash grids followed by a tiny MLP to represent color. Here, we input positions into the hash grids, and then the resulting feature and the view direction are fed into the MLP. The result will be used to be converted into RGB colors
- Previous method represents a scene with numerous small Gaussians collectively, and each Gaussian primitive is not expected to show high diversity. In this improvement, we use a codebook-based approach for modeling the geometry of Gaussians. It learns to find similar patterns or geometry shared across each scene and only stores the codebook index for each Gaussian, which helps to reduce spatial and computational resources
# NeRF Synthetic
### Result
|   | Scene  | lego      | mic      | ficus   | chair   | hotdog  | ship     | materials | drums    |
| -------- | -------- | --------- | -------- | ------- | ------- | ------- | -------- | --------- | -------- |
| |SSIM     | 0.98 | 0.99 | 0.98 | 0.98 | 0.98 | 0.90 | 0.96 | 0.95 |
| |PSNR     | 36.05 | 36.78 | 35.49 | 35.53 | 38.06 | 31.67 | 30.49 | 26.28 |
| |LPIPS    | 0.01 | 0.01 | 0.01 | 0.01 | 0.02 | 0.10 | 0.04 | 0.04 |
|3DGS|Storage (MB)|	350.81|	405.94|	331.23|	173.60|	539.08|	360.14|	189.52|	565.76|
| |SSIM     | 0.98 | 0.99 | 0.98 | 0.98 | 0.98 | 0.90 | 0.96 | 0.95 |
| |PSNR     | 37.12 | 36.81 | 35.55 | 36.53 | 38.54 | 33.82 | 31.44 | 30.19 |
| |LPIPS    | 0.02 | 0.01 | 0.01 | 0.01 | 0.02 | 0.11 | 0.04 | 0.04 |
|Ours|Storage (MB)|	48.99|	27.15|	44.78|	50.66|	41.13|	34.51|	36.24|	40.45|
### Visualize
|          | Render Image    | Grouth truth     | 
| -------- | ------- | -------- |
| lego     | ![[Images/improved/lego.png]] | ![[Images/nerf/lego_gt.png]] |
| mic      | ![[Images/improved/mic.png]] | ![[Images/nerf/mic_gt.png]] |
| ficus    | ![[Images/improved/ficus.png]] | ![[Images/nerf/ficus_gt.png]] |
| chair    | ![[Images/improved/chair.png]] | ![[Images/nerf/chair_gt.png]] |
| hotdog   | ![[Images/improved/hotdog.png]] | ![[Images/nerf/hotdog_gt.png]] |
| ship     | ![[Images/improved/ship.png]] | ![[Images/nerf/ship_gt.png]] |
| materials| ![[Images/improved/materials.png]] | ![[Images/nerf/materials_gt.png]] |
| drums    | ![[Images/improved/drums.png]] | ![[Images/nerf/drums_gt.png]] |
# MipNeRF 360
### Result

|	|Scene|	bicycle|flowers|garden|stump|tree hill|room|counter|kitchen|bonsai|
| -------- | -------- | ------- | -------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | 
|	|PSNR|	25.10|	21.33|	27.25|	26.66|	22.53|	31.50|	29.11|	31.53|	32.16|	
|	|SSIM|	0.747|	0.588|	0.856|	0.769|	0.635|	0.925|	0.914|	0.932|	0.946|	
|	|LPIPS|	0.244|	0.361|	0.122|	0.243|	0.346|	0.198|	0.184|	0.117|	0.181|	
|3DGS|Storage (MB)|	1350.78|	805.94|	1331.33|	1073.60|	819.08|	350.14|	276.52|	411.76|	295.08|	
|	|PSNR|	24.77|	20.89|	26.81|	26.46|	22.65|	30.88|	28.71|	30.48|	32.08|	
|	|SSIM|	0.723|	0.556|	0.832|	0.757|	0.638|	0.919|	0.902|	0.919|	0.939|	
|	|LPIPS|	0.286|	0.399|	0.161|	0.278|	0.363|	0.209|	0.205|	0.131|	0.193|	
|Ours|Storage (MB)|	62.99|	51.15|	62.78|	54.66|	59.33|	34.21|	34.34|	44.45|	35.44|
	
### Visualize
|          | Render Image    | Grouth truth     | 
| -------- | ------- | -------- |
| bicycle  | ![[Images/improved/bicycle.png]] | ![[Images/mipnerf360/bicycle_gt.png]] |
| bonsai   | ![[Images/improved/bonsai.png]] | ![[Images/mipnerf360/bonsai_gt.png]] |
| counter  | ![[Images/improved/counter.png]] | ![[Images/mipnerf360/counter_gt.png]] |
| garden   | ![[Images/improved/garden.png]] | ![[Images/mipnerf360/garden_gt.png]] |
| kitchen  | ![[Images/improved/kitchen.png]] | ![[Images/mipnerf360/kitchen_gt.png]] |
| stump    | ![[Images/improved/stump.png]] | ![[Images/mipnerf360/stump_gt.png]] |
| room     | ![[Images/improved/room.png]] | ![[Images/mipnerf360/room_gt.png]] |
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

