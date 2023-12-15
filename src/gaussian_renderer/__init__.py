#
# Copyright (C) 2023, Inria
# GRAPHDECO research group, https://team.inria.fr/graphdeco
# All rights reserved.
#
# This software is free for non-commercial, research and evaluation use 
# under the terms of the LICENSE.md file.
#
# For inquiries contact  george.drettakis@inria.fr
#

import torch
import math
import numpy as np
from diff_gaussian_rasterization import GaussianRasterizationSettings, GaussianRasterizer
# from scene.gaussian_model import GaussianModel
# from utils.sh_utils import eval_sh
import pickle
def save_tensors(file_path, var_dict):
    for var in var_dict.keys():
        torch.save(var_dict[var],f'{file_path}/{var}.pt')
        try:
            np.savetxt(f'{file_path}/{var}.txt', var_dict[var].detach().cpu().numpy(),fmt="%s", header=str(var_dict[var].shape))
        except:
            np.savetxt(f'{file_path}/{var}.txt', var_dict[var].detach().cpu().numpy().reshape((3,-1)), fmt="%s", header=str(var_dict[var].shape))
        print(f'Saved {var}')
def load_tensors(file_path,var_dict):
    for var in var_dict.keys():
        var_dict[var]=torch.load(f'{file_path}/{var}.pt',map_location=lambda storage, loc: storage.cuda(0))
        print(f'Load {var}')
    return var_dict
def save_inputs(file_path, viewpoint_camera, gaussian):
    data = {
        "viewpoint_camera": viewpoint_camera,
        "gaussian": gaussian
    }
    with open(file_path, 'wb') as file:
        pickle.dump(data, file,protocol=pickle.HIGHEST_PROTOCOL)

# Function to load inputs (viewpoint_camera, gaussian, and other tensors)
def load_inputs(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data["viewpoint_camera"], data["gaussian"]

def render(viewpoint_camera, pc , pipe, bg_color : torch.Tensor, scaling_modifier = 1.0, override_color = None, visualize=False):
    """
    Render the scene. 
    
    Background tensor (bg_color) must be on GPU!
    """
    '''
    DEBUG
    '''
    # Create zero tensor. We will use it to make pytorch return gradients of the 2D (screen-space) means
    screenspace_points = torch.zeros_like(pc.get_xyz, dtype=pc.get_xyz.dtype, requires_grad=True, device="cuda:0") + 0
    try:
        screenspace_points.retain_grad()
    except:
        pass

    # Set up rasterization configuration
    tanfovx = math.tan(viewpoint_camera.FoVx * 0.5)
    tanfovy = math.tan(viewpoint_camera.FoVy * 0.5)

   
    raster_settings = GaussianRasterizationSettings(
        image_height=int(viewpoint_camera.image_height),
        image_width=int(viewpoint_camera.image_width),
        tanfovx=tanfovx,
        tanfovy=tanfovy,
        bg=bg_color,
        scale_modifier=scaling_modifier,
        viewmatrix=viewpoint_camera.world_view_transform,
        projmatrix=viewpoint_camera.full_proj_transform,
        sh_degree=pc.active_sh_degree,
        campos=viewpoint_camera.camera_center,
        prefiltered=False,
        debug=pipe.debug
    )

    rasterizer = GaussianRasterizer(raster_settings=raster_settings)

    means3D = pc.get_xyz
    means2D = screenspace_points
    opacity = pc.get_opacity
    
    if visualize:
        # DEBUG: To view Gaussian epllipsoid
        threshold = 0.05
        gauss_opacity = opacity.clone()
        gauss_opacity[gauss_opacity>=threshold]=1.0
        gauss_opacity[gauss_opacity<threshold]=0.0

    # If precomputed 3d covariance is provided, use it. If not, then it will be computed from
    # scaling / rotation by the rasterizer.
    scales = None
    rotations = None
    cov3D_precomp = None
    if pipe.compute_cov3D_python:
        cov3D_precomp = pc.get_covariance(scaling_modifier)
    else:
        scales = pc.get_scaling
        rotations = pc.get_rotation

    # If precomputed colors are provided, use them. Otherwise, if it is desired to precompute colors
    # from SHs in Python, do it. If not, then SH -> RGB conversion will be done by rasterizer.
    shs = None
    colors_precomp = None
    if override_color is None:
        if pipe.convert_SHs_python:
            shs_view = pc.get_features.transpose(1, 2).view(-1, 3, (pc.max_sh_degree+1)**2)
            dir_pp = (pc.get_xyz - viewpoint_camera.camera_center.repeat(pc.get_features.shape[0], 1))
            dir_pp_normalized = dir_pp/dir_pp.norm(dim=1, keepdim=True)
            sh2rgb = eval_sh(pc.active_sh_degree, shs_view, dir_pp_normalized)
            colors_precomp = torch.clamp_min(sh2rgb + 0.5, 0.0)
        else:
            shs = pc.get_features
    else:
        colors_precomp = override_color
    
    # Rasterize visible Gaussians to image, obtain their radii (on screen). 
    rendered_image, radii = rasterizer(
        means3D = means3D,
        means2D = means2D,
        shs = shs,
        colors_precomp = colors_precomp,
        opacities = opacity,
        scales = scales,
        rotations = rotations,
        cov3D_precomp = cov3D_precomp)
    if visualize:
        # DEBUG: To view Gaussian epllipsoid
        gaussian_image, gaussian_radii = rasterizer(
            means3D = means3D,
            means2D = means2D,
            shs = shs,
            colors_precomp = colors_precomp,
            opacities = gauss_opacity,
            scales = scales,
            rotations = rotations,
            cov3D_precomp = cov3D_precomp)
    else:
        gaussian_image=None

        # Those Gaussians that were frustum culled or had a radius of 0 were not visible.
        # They will be excluded from value updates used in the splitting criteria.
    return {"render": rendered_image,
                "gaussian": gaussian_image,
                "viewspace_points": screenspace_points,
                "visibility_filter" : radii > 0,
                "radii": radii}

if __name__=='__main__':
    torch.set_printoptions(threshold=10_000)
    import sys
    sys.path.insert(0, '..')
    from scene.gaussian_model import GaussianModel
    from scene.cameras import Camera

    gaussian=GaussianModel(sh_degree=3)
    viewpoint_camera=Camera()

    viewpoint_camera, gaussian = load_inputs('../render_inputs.pkl')

    from typing import NamedTuple

    class pipe(NamedTuple):
        debug: bool
        convert_SHs_python: bool
        compute_cov3D_python : bool
    
    opt=pipe(debug=False,compute_cov3D_python=False,convert_SHs_python=False)
    bg_color = torch.FloatTensor([1, 1, 1]).cuda()
    
    
    # Call the render function
    result = render(viewpoint_camera, gaussian,opt,bg_color)
    print(result)

