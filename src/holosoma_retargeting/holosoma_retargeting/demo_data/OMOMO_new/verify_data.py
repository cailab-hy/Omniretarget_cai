
import torch
import numpy as np

file_path = '/home/cai/holosoma/src/holosoma_retargeting/holosoma_retargeting/demo_data/OMOMO_new/sub10_largebox_049.pt'
data = torch.load(file_path, map_location='cpu')

# Region 1: 0 - 162 (Hypothesis: Joint Angles/Root)
# 0-3: Root Pos?
# 3-6: Root Rot?
# 6-162: Joint Angles?
root_pos = data[:, 0:3]
print(f"Region 1 [0:3] (Root Pos?) Range: {root_pos.min().item():.3f} to {root_pos.max().item():.3f}")
print(f"Region 1 [0:3] Mean: {root_pos.mean(dim=0)}")
print(f"Region 1 [0:3] Std: {root_pos.std(dim=0)}")

root_rot = data[:, 3:6]
print(f"Region 1 [3:6] (Root Rot?) Range: {root_rot.min().item():.3f} to {root_rot.max().item():.3f}")

joint_angles = data[:, 6:162]
print(f"Region 1 [6:162] (Joint Ang?) Range: {joint_angles.min().item():.3f} to {joint_angles.max().item():.3f}")

# Region 4: 325 - 591 (Hypothesis: Env/Heightmap + Goal)
# 591 - 325 = 266.
# Maybe 266 = 256 (Heightmap) + 10 (Goal)?
# Check last 10 dims
last_10 = data[:, -10:]
print(f"Region 4 [-10:] Range: {last_10.min().item():.3f} to {last_10.max().item():.3f}")
print(f"Region 4 [-10:] Values (first frame): {last_10[0]}")

# Check first 256 dims of Region 4
heightmap = data[:, 325:325+256]
print(f"Region 4 [0:256] Range: {heightmap.min().item():.3f} to {heightmap.max().item():.3f}")
print(f"Region 4 [0:256] Mean: {heightmap.mean().item():.3f}")
