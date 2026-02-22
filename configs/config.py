import os
import json
import logging
import itertools
from typing import Dict, Any, List, Tuple
from datetime import datetime

from pydantic import BaseModel
from pprint import pformat

from utils.tools import load_yaml_config, load_json_file
from utils.logger import get_logging_level, setup_logger

logger = setup_logger("Config", logging.INFO)

class ConfigBase(BaseModel):
    game_setups_path: str
    verifier_config_path: str
    game_prompt_names: Dict[str, str]

    log_level: int = logging.INFO
    
class SingleGameConfigBase(BaseModel):
    """single game config base"""
    model_name: str
    model_provider: str
    setup_id: str
    game_result_save_folder: str
    max_rounds: int
    with_reasoning: bool
    with_hint: bool
    mode: str
    prompt_context_mode: str = "turnbench_default"
    memory_budget_tokens: int = 2048
    memory_strategy: str = "full_history"
    distractor_mode: str = "none"
    distractor_tokens: int = 0

class SingleGameConfig(SingleGameConfigBase, ConfigBase):
    """single game config"""
    pass

class ExperimentConfig(ConfigBase):
    """experiment config"""
    num_threads: int
    all_experiments: List[SingleGameConfigBase]

def get_nested_dict_counter(dimensions: Tuple, current_level: int, max_level: int) -> Dict:
    """create nested dict in safe way"""
    if current_level == max_level:
        return 0
    
    result = {}
    for item in dimensions[current_level]:
        result[item] = get_nested_dict_counter(dimensions, current_level + 1, max_level)
    return result

def build_error_list_config(yaml_config: Dict[str, Any]) -> ExperimentConfig:
    """build error list config"""
    error_list_yaml_config = yaml_config["error_list_config"]
    error_list = load_json_file(error_list_yaml_config.get("error_list_path"))
    game_prompt_names = yaml_config["game_prompt_names"]
    all_experiments = []

    for experiment_config in error_list:
        all_experiments.append(SingleGameConfigBase(**experiment_config))

    return ExperimentConfig(
        game_setups_path=error_list_yaml_config.get("game_setups_path"),
        verifier_config_path=error_list_yaml_config.get("verifier_config_path"),
        game_prompt_names=game_prompt_names,
        num_threads=error_list_yaml_config.get("num_threads"),
        log_level=get_logging_level(error_list_yaml_config.get("log_level")),
        all_experiments=all_experiments
    )
    
def build_experiment_config(yaml_config: Dict[str, Any]) -> ExperimentConfig:
    """build experiment config"""
    experiment_yaml_config = yaml_config["experiment_config"]
    game_setups = load_json_file(experiment_yaml_config["game_setups_path"])
    game_prompt_names = yaml_config["game_prompt_names"]
    all_experiments = []
    game_setup_ids = list(game_setups.keys())
    mode_options = experiment_yaml_config.get("mode", [])
    reasoning_options = experiment_yaml_config.get("with_reasoning", [])
    hint_options = experiment_yaml_config.get("with_hint", [])
    model_names = experiment_yaml_config.get("model_names", [])
    model_providers = experiment_yaml_config.get("model_providers", [])
    model_pairs = list(zip(model_names, model_providers))
    combinations = itertools.product(
        mode_options,
        reasoning_options,
        hint_options,
        model_pairs,
        game_setup_ids
    )
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    break_point_folder_path = experiment_yaml_config.get("break_point_folder_path", None)
    all_existing_experiment_paths = {}
    if break_point_folder_path:
        current_datetime = os.path.basename(break_point_folder_path)
        all_existing_experiment_paths = {
            os.path.join(root, file): True 
            for root, _, files in os.walk(break_point_folder_path) 
            for file in files
            if root != break_point_folder_path
        }

    existing_experiment_counter = get_nested_dict_counter(
        (model_names, mode_options, ["reasoning", "no_reasoning"]), 0, 3)
    new_experiment_counter = get_nested_dict_counter(
        (model_names, mode_options, ["reasoning", "no_reasoning"]), 0, 3)
    for mode, reasoning, hint, model_pair, setup_id in combinations:
        model, provider = model_pair
        reasoning_str = "reasoning" if reasoning else "no_reasoning"
        hint_str = "hint" if hint else "no_hint"
        save_path = os.path.join(
            experiment_yaml_config["game_result_save_folder"],
            current_datetime,
            mode,
            f"{reasoning_str}_{hint_str}",
            f"{model}_{provider}_{setup_id}.json"
        )
        if all_existing_experiment_paths.get(save_path, False):
            existing_experiment_counter[model][mode][reasoning_str] += 1
            continue

        new_experiment_counter[model][mode][reasoning_str] += 1
        all_experiments.append(SingleGameConfigBase(
            mode=mode,
            with_reasoning=reasoning,
            with_hint=hint,
            model_name=model,
            model_provider=provider,
            setup_id=setup_id,
            game_result_save_folder=save_path,
            max_rounds=experiment_yaml_config["max_rounds"]
        ))

    logger.info(f"Found {len(all_existing_experiment_paths)} existing experiments in {break_point_folder_path}")
    logger.info(f"Existing experiment details: \n{pformat(existing_experiment_counter)}\n")
    logger.info(f"Created {len(all_experiments)} new experiments")
    logger.info(f"New experiment details: \n{pformat(new_experiment_counter)}\n")

    return ExperimentConfig(
        game_setups_path=experiment_yaml_config["game_setups_path"],
        verifier_config_path=experiment_yaml_config["verifier_config_path"],
        game_prompt_names=game_prompt_names,
        num_threads=experiment_yaml_config["num_threads"],
        log_level=get_logging_level(experiment_yaml_config["log_level"]),
        all_experiments=all_experiments
    )

def build_single_game_config(yaml_config: Dict[str, Any]) -> SingleGameConfig:
    """build single game config"""
    single_game_config = yaml_config["single_game_config"]
    single_game_config["log_level"] = get_logging_level(single_game_config["log_level"])
    game_prompt_names = yaml_config["game_prompt_names"]
    return SingleGameConfig(**{**single_game_config, "game_prompt_names": game_prompt_names})

def get_config(config_path: str) -> BaseModel:
    """get config for single game or experiment"""
    yaml_config = load_yaml_config(config_path)
    if yaml_config.get("running_mode") == "single_game":
        logger.info(f"Running in single game mode\n")
        return "single_game", build_single_game_config(yaml_config)
    elif yaml_config.get("running_mode") == "experiment":
        logger.info(f"Running in experiment mode\n")
        return "experiment", build_experiment_config(yaml_config)
    elif yaml_config.get("running_mode") == "error_list":
        logger.info(f"Running in error list mode\n")
        return "error_list", build_error_list_config(yaml_config)
    else:
        raise ValueError(f"Invalid running mode: {yaml_config.get('running_mode')}")
