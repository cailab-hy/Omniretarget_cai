from dataclasses import replace

from holosoma.config_types.experiment import ExperimentConfig, NightlyConfig, TrainingConfig
from holosoma.config_values import (
    action,
    algo,
    robot,
    simulator,
    terrain,
)
from holosoma.config_values.wbt.walker import command, curriculum, observation, randomization, reward, termination

walker_30dof_wbt = ExperimentConfig(
    training=TrainingConfig(
        project="WholeBodyTracking",
        name="walker_30dof_wbt_manager",
        num_envs=8192,
    ),
    env_class="holosoma.envs.wbt.wbt_manager.WholeBodyTrackingManager",
    algo=replace(
        algo.ppo,
        config=replace(
            algo.ppo.config,
            num_learning_iterations=40000,
            save_interval=4000,
            entropy_coef=0.005,
            init_noise_std=1.0,
            init_at_random_ep_len=False,
            use_symmetry=False,
            actor_optimizer=replace(algo.ppo.config.actor_optimizer, weight_decay=0.000),
            critic_optimizer=replace(algo.ppo.config.critic_optimizer, weight_decay=0.000),
        ),
    ),
    simulator=replace(
        simulator.isaacsim,
        config=replace(
            simulator.isaacsim.config,
            sim=replace(
                simulator.isaacsim.config.sim,
                max_episode_length_s=10.0,
            ),
        ),
    ),
    robot=replace(
        robot.walker_30dof,
        control=replace(robot.walker_30dof.control, action_scale=1.0),
        asset=replace(robot.walker_30dof.asset, enable_self_collisions=True),
        init_state=replace(robot.walker_30dof.init_state, pos=[0.0, 0.0, 1.0]),
    ),
    terrain=terrain.terrain_locomotion_plane,
    observation=observation.walker_30dof_wbt_observation,
    action=action.g1_29dof_joint_pos,  # Action is robot-agnostic
    termination=termination.walker_30dof_wbt_termination,
    randomization=randomization.walker_30dof_wbt_randomization,
    command=command.walker_30dof_wbt_command,
    curriculum=curriculum.walker_30dof_wbt_curriculum,
    reward=reward.walker_30dof_wbt_reward,
    nightly=NightlyConfig(
        iterations=8000,
        metrics={
            "Episode/rew_motion_global_ref_position_error_exp": [0.16, "inf"],
            "Episode/rew_motion_global_ref_orientation_error_exp": [0.20, "inf"],
            "Episode/rew_motion_relative_body_position_error_exp": [0.45, "inf"],
            "Episode/rew_motion_relative_body_orientation_error_exp": [0.30, "inf"],
            "Episode/rew_motion_global_body_lin_vel": [0.30, "inf"],
            "Episode/rew_motion_global_body_ang_vel": [0.02, "inf"],
        },
    ),
)

walker_30dof_wbt_w_object = replace(
    walker_30dof_wbt,
    command=command.walker_30dof_wbt_command_w_object,
    robot=replace(
        robot.walker_30dof_w_object,
        asset=replace(
            robot.walker_30dof_w_object.asset,
            enable_self_collisions=True,
        ),
        object=replace(
            robot.walker_30dof_w_object.object,
            object_urdf_path="holosoma/data/motions/walker_30dof/whole_body_tracking/objects_suitcase.urdf",
        ),
        init_state=replace(robot.walker_30dof_w_object.init_state, pos=[0.0, 0.0, 1.0]),
    ),
    randomization=randomization.walker_30dof_wbt_randomization_w_object,
    observation=observation.walker_30dof_wbt_observation_w_object,
    reward=reward.walker_30dof_wbt_reward_w_object,
    simulator=replace(
        simulator.isaacsim,
        config=replace(simulator.isaacsim.config, scene=replace(simulator.isaacsim.config.scene, env_spacing=0.0)),
    ),
)

__all__ = [
    "walker_30dof_wbt",
    "walker_30dof_wbt_w_object",
]


"""
Example 1: Robot only:
python src/holosoma/holosoma/train_agent.py \\
    exp:walker-30dof-wbt

Example 2: Robot+Object:
python src/holosoma/holosoma/train_agent.py \\
    exp:walker-30dof-wbt-w-object \\
    simulator:isaacsim \\
    logger:wandb-wbt \\
    --logger.base-dir logs \\
    --command.setup_terms.motion_command.params.motion_config.motion_file="/home/cai/holosoma/src/holosoma/holosoma/data/motions/walker_30dof/whole_body_tracking/sub1_suitcase_011_mj_w_obj.npz"

Note: Use logger:wandb-wbt instead of logger:wandb to disable command overlay (WBT doesn't use locomotion commands)
"""
