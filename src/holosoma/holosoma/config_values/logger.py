from holosoma.config_types.logger import DisabledLoggerConfig, WandbLoggerConfig
from holosoma.config_types.video import VideoConfig

disabled = DisabledLoggerConfig()

wandb = WandbLoggerConfig(mode="online")

wandb_offline = WandbLoggerConfig(mode="offline")

# WBT experiments don't have locomotion commands, so disable command overlay
wandb_wbt = WandbLoggerConfig(mode="online", video=VideoConfig(show_command_overlay=False))

DEFAULTS = {
    "disabled": disabled,
    "wandb": wandb,
    "wandb-wbt": wandb_wbt,
    "wandb_offline": wandb_offline,
}
