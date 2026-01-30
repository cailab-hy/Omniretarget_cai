"""
Visualize a converted motion npz file in MuJoCo.

Usage:
    python data_conversion/visualize_converted_motion.py \
        --motion-file converted_res/walker/object_interaction/sub1_suitcase_011_mj_w_obj.npz \
        --robot walker \
        --object-name suitcase
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import mujoco
import mujoco.viewer as mjv
import numpy as np


def main():
    parser = argparse.ArgumentParser(description="Visualize converted motion data in MuJoCo")
    parser.add_argument("--motion-file", type=str, required=True, help="Path to the converted .npz file")
    parser.add_argument("--robot", type=str, default="walker", help="Robot type (default: walker)")
    parser.add_argument("--object-name", type=str, default=None, help="Object name (e.g., suitcase, largebox)")
    parser.add_argument("--loop", action="store_true", help="Loop the motion forever")
    args = parser.parse_args()

    # Load motion data
    data = np.load(args.motion_file, allow_pickle=True)
    joint_pos = data["joint_pos"]  # (num_frames, num_qpos) - robot only
    joint_vel = data["joint_vel"]  # (num_frames, num_qvel) - robot only
    fps = data["fps"][0] if "fps" in data else 50
    dt = 1.0 / fps

    # Check if object data exists and combine with robot data
    has_object = "object_pos_w" in data and "object_quat_w" in data
    if has_object:
        object_pos = data["object_pos_w"]  # (num_frames, 3)
        object_quat = data["object_quat_w"]  # (num_frames, 4)
        object_lin_vel = data.get("object_lin_vel_w", np.zeros((joint_pos.shape[0], 3)))
        object_ang_vel = data.get("object_ang_vel_w", np.zeros((joint_pos.shape[0], 3)))
        
        # Combine: robot qpos + object pos + object quat
        joint_pos = np.concatenate([joint_pos, object_pos, object_quat], axis=1)
        joint_vel = np.concatenate([joint_vel, object_lin_vel, object_ang_vel], axis=1)
        print(f"  Object data found, combined qpos dim: {joint_pos.shape[1]}")

    print(f"Loaded motion: {args.motion_file}")
    print(f"  Frames: {joint_pos.shape[0]}, FPS: {fps}")
    print(f"  qpos dim: {joint_pos.shape[1]}, qvel dim: {joint_vel.shape[1]}")

    # Determine XML path
    # Assuming standard path structure: models/<robot>/<robot>_<dof>dof[_w_<object>].xml
    models_dir = Path(__file__).resolve().parent.parent / "models"
    
    if args.robot == "walker":
        robot_dof = 30
    elif args.robot == "g1":
        robot_dof = 29
    else:
        robot_dof = 29  # default

    if args.object_name:
        xml_path = models_dir / args.robot / f"{args.robot}_{robot_dof}dof_w_{args.object_name}.xml"
    else:
        xml_path = models_dir / args.robot / f"{args.robot}_{robot_dof}dof.xml"

    print(f"Loading model: {xml_path}")
    model = mujoco.MjModel.from_xml_path(str(xml_path))
    mj_data = mujoco.MjData(model)

    # Check dimensions match
    if joint_pos.shape[1] != model.nq:
        print(f"Warning: qpos dimension mismatch! Data has {joint_pos.shape[1]}, model expects {model.nq}")
    if joint_vel.shape[1] != model.nv:
        print(f"Warning: qvel dimension mismatch! Data has {joint_vel.shape[1]}, model expects {model.nv}")

    # Launch viewer
    viewer = mjv.launch_passive(model, mj_data, show_left_ui=False, show_right_ui=False)
    viewer.cam.distance = 2.5
    viewer.cam.elevation = -20.0
    viewer.cam.azimuth = 45.0

    print(f"\nPlaying motion... (Press Ctrl+C to stop)")
    
    try:
        while True:
            for i in range(joint_pos.shape[0]):
                start = time.perf_counter()

                # Set state
                mj_data.qpos[:] = joint_pos[i]
                mj_data.qvel[:] = joint_vel[i]
                mujoco.mj_forward(model, mj_data)
                viewer.sync()

                # Maintain FPS
                elapsed = time.perf_counter() - start
                time.sleep(max(0, dt - elapsed))

                if not viewer.is_running():
                    return

            if not args.loop:
                print("Motion playback complete.")
                break

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        viewer.close()


if __name__ == "__main__":
    main()
