"""Whole Body Tracking termination presets for the Walker robot."""

from holosoma.config_types.termination import TerminationManagerCfg, TerminationTermCfg

walker_30dof_wbt_termination = TerminationManagerCfg(
    terms={
        "timeout": TerminationTermCfg(
            func="holosoma.managers.termination.terms.common:timeout_exceeded",
            is_timeout=True,
        ),
        "motion_ends": TerminationTermCfg(
            func="holosoma.managers.termination.terms.wbt:motion_ends",
        ),
        "bad_tracking": TerminationTermCfg(
            func="holosoma.managers.termination.terms.wbt:BadTracking",
            params={
                # robot tracking
                "bad_ref_pos_threshold": 0.5,
                "bad_ref_ori_threshold": 0.8,
                "bad_motion_body_pos_threshold": 0.25,
                # NOTE: body_names_to_track is shared with command_manager
                "body_names_to_track": [
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
                "bad_motion_body_pos_body_names": [
                    "ankle_roll_l_link",
                    "ankle_roll_r_link",
                    "wrist_roll_l_link",
                    "wrist_roll_r_link",
                ],
                # object tracking
                # only triggered when has_object=True
                "bad_object_pos_threshold": 1.0,  # 0.25 default
                "bad_object_ori_threshold": 0.8,
            },
        ),
    }
)

__all__ = ["walker_30dof_wbt_termination"]
