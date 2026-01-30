"""Whole Body Tracking command presets for the Walker robot."""

from dataclasses import replace

from holosoma.config_types.command import (
    CommandManagerCfg,
    CommandTermCfg,
    MotionConfig,
    NoiseToInitialPoseConfig,
)

init_pose_config = NoiseToInitialPoseConfig(
    overall_noise_scale=1.0,
    dof_pos=0.1,
    root_pos=[0.05, 0.05, 0.01],
    root_rot=[0.1, 0.1, 0.2],
    root_lin_vel=[0.1, 0.1, 0.05],
    root_ang_vel=[0.1, 0.1, 0.1],
    object_pos=[0.05, 0.05, 0.0],
)

motion_config = MotionConfig(
    motion_file="holosoma/data/motions/walker_30dof/whole_body_tracking/sub1_suitcase_011_mj.npz",
    body_names_to_track=[
        "pelvis",
        "hip_pitch_l_link",
        "knee_pitch_l_link",
        "ankle_roll_l_link",
        "hip_pitch_r_link",
        "knee_pitch_r_link",
        "ankle_roll_r_link",
        "body_yaw_link",
        "shoulder_roll_l_link",
        "elbow_pitch_l_link",
        "wrist_roll_l_link",
        "shoulder_roll_r_link",
        "elbow_pitch_r_link",
        "wrist_roll_r_link",
    ],
    body_name_ref=["body_yaw_link"],
    use_adaptive_timesteps_sampler=False,
    noise_to_initial_pose=init_pose_config,
)

motion_config_w_object = replace(
    motion_config,
    motion_file="holosoma/data/motions/walker_30dof/whole_body_tracking/sub1_suitcase_011_mj_w_obj.npz",
)

walker_30dof_wbt_command = CommandManagerCfg(
    params={},
    setup_terms={
        "motion_command": CommandTermCfg(
            func="holosoma.managers.command.terms.wbt:MotionCommand",
            params={
                "motion_config": motion_config,
            },
        ),
    },
    reset_terms={
        "motion_command": CommandTermCfg(
            func="holosoma.managers.command.terms.wbt:MotionCommand",
        )
    },
    step_terms={
        "motion_command": CommandTermCfg(
            func="holosoma.managers.command.terms.wbt:MotionCommand",
        )
    },
)

walker_30dof_wbt_command_w_object = replace(
    walker_30dof_wbt_command,
    setup_terms={
        "motion_command": CommandTermCfg(
            func="holosoma.managers.command.terms.wbt:MotionCommand",
            params={
                "motion_config": motion_config_w_object,
            },
        )
    },
)

__all__ = [
    "walker_30dof_wbt_command",
    "walker_30dof_wbt_command_w_object",
]
