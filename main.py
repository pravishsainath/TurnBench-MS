from dotenv import load_dotenv

from core.experiment_manager import ExperimentManager
from configs.config import get_config

load_dotenv()

def main():
    config_path = "configs/game_config.yaml"
    running_mode, config = get_config(config_path)
    experiment_manager = ExperimentManager(
        config.game_setups_path,
        config.verifier_config_path,
        config.game_prompt_names,
        config.log_level
    )
    if running_mode == "single_game":
        experiment_manager.run_single_experiment(config)
    elif running_mode == "experiment" or running_mode == "error_list":
        experiment_manager.run_all_experiments(config)
    else:
        raise ValueError(f"Invalid running mode: {running_mode}")


if __name__ == "__main__":
    main()
