from typing import Dict, List, Any, Optional
import concurrent.futures
import logging
import time
import os

from core.game_loop import GameLoop
from core.game_setup_manager import GameSetupManager
from core.game_session import GameSession
from llm.llm_manager import LLMManager
from verifier.verifier_manager import VerifierManager
from prompt.prompt_manager import PromptManager
from configs.config import SingleGameConfigBase, ExperimentConfig
from models.prompt import PromptModel
from utils.logger import setup_logger
from utils.tools import save_json_file, load_json_file

class ExperimentManager:
    """
    Experiment manager, responsible for setting up and running multi-round game experiments
    Supports comparison experiments with multiple models
    """
    
    def __init__(
        self, 
        game_setups_path: str, 
        verifier_config_path: str, 
        game_prompt_names: Dict[str, str],
        log_level: int = logging.INFO
    ) -> None:
        """Initialize experiment manager"""
        self.llm_manager = LLMManager()
        self.prompt_manager = PromptManager()
        self.game_setup_manager = GameSetupManager.from_json(game_setups_path)
        self.verifier_manager = VerifierManager.from_json(verifier_config_path)
        self.game_prompt_names = game_prompt_names
        self.log_level = log_level
        self.logger = setup_logger("ExperimentManager", self.log_level)
        self.existing_success_list = []
        self.existing_error_list = []

    def build_prompt_model(self, config: SingleGameConfigBase) -> PromptModel:
        """Build the prompt model"""
        try:
            prompts = {}
            for prompt_category, prompt_name in self.game_prompt_names.items():
                if prompt_category == "system_prompt":
                    current_prompt_name = f"{config.mode}_{prompt_name}"
                else:
                    current_prompt_name = (
                        f"{config.mode}_{prompt_name}"
                        f"{'_with_reasoning' if config.with_reasoning else ''}"
                        f"{'_with_hint' if config.with_hint else ''}"
                    )
                prompts[prompt_category] = self.prompt_manager.get_prompt(current_prompt_name)
            prompt_model = PromptModel(**prompts)
            return prompt_model
        except Exception as e:
            raise ValueError(f"Error building prompt model: {e}")

    def run_single_experiment(self, config: SingleGameConfigBase) -> None:
        """Run single experiment"""
        # init prompt
        game_prompts = self.build_prompt_model(config)
        # init llm client
        llm_client = self.llm_manager.get_client(config.model_provider)
        provider_model_name = self.llm_manager.get_provider_model_name(config.model_name, config.model_provider)
        # init game setup
        game_setup = self.game_setup_manager.load_setup(config.setup_id)
        # init verifier
        verifier_descriptions = self.verifier_manager.get_verifier_descriptions(game_setup.verifier_ids)
        # init main game session
        game_session = GameSession(log_level=self.log_level)
        game_session.initialize(provider_model_name, config, game_setup, game_prompts, verifier_descriptions)
        # init game loop
        game_loop = GameLoop(game_session, llm_client, self.verifier_manager, self.log_level)
        game_loop.run()
     
    
    def run_all_experiments(self, config: ExperimentConfig) -> None:
        """Run all experiments"""
        experiments: List[SingleGameConfigBase] = config.all_experiments
        num_threads: int = config.num_threads
        if len(experiments) == 0:
            return
        save_folder = config.all_experiments[0].game_result_save_folder
        save_folder = os.path.join(*os.path.normpath(save_folder).split(os.sep)[:3])
        os.makedirs(save_folder, exist_ok=True)

        progress_report_interval = 2 if len(experiments) < 10 else 20
        start_time = time.time()
        if num_threads <= 0:
            self.logger.warning("Threads number must be positive. Using single thread.")
            num_threads = 1
        max_workers = num_threads

        self.logger.info(f"Start running {len(experiments)} experiments with {max_workers} threads...\n")

        success_list = []
        error_list = []
        if os.path.exists(os.path.join(save_folder, "success_list.json")):
            self.existing_success_list = load_json_file(os.path.join(save_folder, "success_list.json"))
        if os.path.exists(os.path.join(save_folder, "error_list.json")):
            self.existing_error_list = load_json_file(os.path.join(save_folder, "error_list.json"))

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_config = {executor.submit(self.run_single_experiment, exp_config): exp_config for exp_config in experiments}

            completed_count = 0
            success_count = 0
            error_count = 0
            for future in concurrent.futures.as_completed(future_to_config):
                exp_config = future_to_config[future]
                exp_config_dump = exp_config.model_dump()
                try:
                    future.result()
                    success_count += 1
                    success_list.append(exp_config_dump)
                    if exp_config_dump in self.existing_error_list:
                        self.existing_error_list.remove(exp_config_dump)
                    self.logger.debug(f"Experiment {exp_config.setup_id} (Model: {exp_config.model_name}, Mode: {exp_config.mode}) completed. ({success_count}/{len(experiments)})")
                except Exception as exc:
                    error_count += 1
                    error_list.append(exp_config_dump)
                    self.logger.error(f"Experiment configuration {exp_config.game_result_save_folder} generated an exception: {exc}")
                finally:
                    completed_count += 1
                    if completed_count % progress_report_interval == 0:
                        self.logger.info((
                            f"\nCompleted {completed_count} experiments, Success: {success_count}, Failed: {error_count}\n"
                            f"Progress: ({completed_count}/{len(experiments)})"
                        ))
                        self.save_error_experiments_progress(self.existing_error_list, save_folder)

        end_time = time.time()
        self.logger.info(f"All {len(experiments)} experiments completed. Time taken: {end_time - start_time} seconds")
        self.save_experiment_progress(success_list, error_list, save_folder)

    def save_experiment_progress(self, success_list: List, error_list: List, save_folder: str) -> None:
        self.save_success_experiments_progress(success_list, save_folder)
        if len(self.existing_error_list) != len(error_list):
            self.logger.error(f"Error list length mismatch. Expected {len(self.existing_error_list)}, got {len(error_list)}")
        self.save_error_experiments_progress(error_list, save_folder)
    
    def save_success_experiments_progress(self, success_list: List, save_folder: str) -> None:
        save_json_file(self.existing_success_list + success_list, os.path.join(save_folder, "success_list.json"))
        self.logger.info(f"Success list with {len(self.existing_success_list + success_list)} experiments, saved to {os.path.join(save_folder, 'success_list.json')}")

    def save_error_experiments_progress(self, error_list: List, save_folder: str) -> None:
        save_json_file(error_list, os.path.join(save_folder, "error_list.json"))
        self.logger.info(f"Error list with {len(error_list)} experiments, saved to {os.path.join(save_folder, 'error_list.json')}")