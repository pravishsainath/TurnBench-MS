import os
import json
import logging
from typing import Optional, Dict, List, Any, Tuple

import uuid

from configs.config import SingleGameConfigBase
from utils.logger import setup_logger
from models.prompt import PromptModel
from models.llm import LLMResponseUsageModel
from models.game import (
    RoundResultModel, 
    ProposalResultModel,
    QuestionResultModel,
    DeduceResultModel,
    GameStateModel, 
    GameSetupModel
)

class GameSession:
    """
    Manage all data for a single game
    """

    def __init__(
        self, 
        session_id: Optional[str] = str(uuid.uuid4()), 
        log_level: int = logging.INFO
    ) -> None:
        """Initialize game session"""
        self.session_id: str = session_id               # Game session ID
        self.experiment_id: str = ""                    # Experiment ID
        self.model_name: str = ""                       # Model name
        self.model_provider: str = ""
        self.generic_model_name: str = ""
        self.messages: List[Dict[str, Any]] = []        # Message history
        self.game_state: GameStateModel = GameStateModel()
        self.round_result: RoundResultModel = RoundResultModel()
        self.round_history: List[Dict[str, Any]] = []   # Round history
        self.setup: GameSetupModel = None               # Game setup
        self.save_folder: Optional[str] = None          # Save folder
        self.max_rounds: int = -1                       # Maximum number of rounds
        self.game_prompts: PromptModel = None           # Game prompt names
        self.verifier_descriptions: str = ""            # Verifier descriptions
        self.logger: logging.Logger = setup_logger("GameSession", log_level)
        
    def initialize(
        self,
        model_name: str,
        game_config: SingleGameConfigBase,
        setup: GameSetupModel,
        game_prompts: PromptModel,
        verifier_descriptions: str,
    ) -> None:
        """Initialize game data"""
        self.model_name = model_name
        self.model_provider = game_config.model_provider
        self.generic_model_name = game_config.model_name
        self.setup = setup
        self.max_rounds = game_config.max_rounds
        self.save_folder = game_config.game_result_save_folder
        self.game_prompts = game_prompts
        self.verifier_descriptions = verifier_descriptions
        self.game_state.with_reasoning = game_config.with_reasoning
        self.game_state.with_hint = game_config.with_hint
        self.game_state.mode = game_config.mode
        self.experiment_id = (
            f"{self.setup.setup_id}_{self.generic_model_name}"
            f"_{self.game_state.mode}"
            f"_{'with_reasoning' if self.game_state.with_reasoning else ''}"
            f"_{'with_hint' if self.game_state.with_hint else ''}"
        )
        # Initialize message history
        self.add_message("system", self.game_prompts.system_prompt.format(
            game_setup=verifier_descriptions))

    def update_game_state_at_round_end(self) -> None:
        """Update game state"""
        self.game_state.total_rounds += 1
        self.game_state.game_over = self.round_result.deduce.submitted
        self.game_state.game_over_reason = "Submitted" if self.round_result.deduce.submitted else None
        self.game_state.success = self.round_result.deduce.guess_correct
        self.game_state.num_of_verifier_passed = self.round_result.deduce.num_of_verifier_passed
        self.game_state.submitted_code = self.round_result.deduce.submitted_code
    
    def update_game_state_when_over_rounds(self) -> None:
        """Update game state when over rounds"""
        self.game_state.game_over = True
        self.game_state.game_over_reason = "Over rounds"
        self.game_state.success = False
        self.game_state.num_of_verifier_passed = self.round_result.deduce.num_of_verifier_passed
        self.game_state.submitted_code = self.round_result.deduce.submitted_code
            
    def update_game_time(self, time_used: float) -> None:
        """Update game time"""
        self.game_state.total_time = time_used
    
    def update_game_response_with_formatting_error(self, count: int = 1) -> None:
        """Update game response with formatting error"""
        self.game_state.total_response_with_formatting_error += count

    def update_game_response_with_not_valid_error(self, count: int = 1) -> None:
        """Update game response with not valid error"""
        self.game_state.total_response_with_not_valid_error += count

    def add_message(self, role: str, content: str) -> None:
        """Add message to history"""
        self.messages.append({"role": role, "content": [{"type": "text", "text": content}]})

    def add_round_result(self) -> None:
        """Add round result"""
        self.round_history.append(self.round_result.model_dump())

    def increment_total_input_tokens(self, count: int = 1) -> None:
        """Increase total input tokens"""
        self.game_state.total_input_tokens += count

    def increment_total_output_tokens(self, count: int = 1) -> None:
        """Increase total output tokens"""
        self.game_state.total_output_tokens += count
    
    def increment_total_prompt_cache_hit_tokens(self, count: int = 1) -> None:
        """Increase prompt cache hit tokens"""
        self.game_state.total_prompt_cache_hit_tokens += count

    def increment_total_reasoning_tokens(self, count: int = 1) -> None:
        """Increase total reasoning tokens"""
        self.game_state.total_reasoning_tokens += count
    
    def update_longest_context_length(self, length: int) -> None:
        """Update longest context length"""
        self.game_state.longest_context_length = max(self.game_state.longest_context_length, length)

    def update_game_tokens(self, usage: LLMResponseUsageModel) -> None:
        """Increase tokens"""
        self.increment_total_input_tokens(usage.input_tokens)
        self.increment_total_output_tokens(usage.output_tokens)
        self.increment_total_reasoning_tokens(usage.reasoning_tokens or 0)
        self.increment_total_prompt_cache_hit_tokens(usage.prompt_cache_hit_tokens or 0)
        self.update_longest_context_length(usage.input_tokens + usage.output_tokens)

    def update_all_guesses(self, guess: str) -> None:
        """Update all guesses"""
        self.game_state.all_guesses.append(guess)

    def update_verifier_uses(self, verifier_choices: List[Tuple[str, str]]) -> None:
        """Update verifier uses"""
        self.game_state.verifier_uses_total += len(verifier_choices)
        self.game_state.all_verifier_choices.append(verifier_choices)

    def refresh_round_result(self) -> None:
        """Refresh round result"""
        self.round_result = RoundResultModel()

    def is_over_rounds(self) -> bool:
        """Check if the game is over rounds"""
        max_rounds = self.max_rounds if self.max_rounds >= 0 else float('inf')
        return self.game_state.total_rounds >= max_rounds

    def check_over_rounds(self) -> bool:
        """Check if the game is over rounds"""
        if self.is_over_rounds():
            self.update_game_state_when_over_rounds()
            return True
        return False

    def is_game_over(self) -> bool:
        """Check if the game is over"""
        return self.game_state.game_over

    def is_success(self) -> bool:
        """Check if the game is successful"""
        return self.game_state.success

    def check_answer(self, final_code: str) -> bool:
        """Check if the final code is correct"""
        return final_code == self.setup.answer

    def get_game_id(self) -> str:
        return f"{self.setup.setup_id}_{self.generic_model_name}_{self.session_id}"

    def update_round_result(
        self, 
        step_name: str, 
        result: ProposalResultModel | List[QuestionResultModel] | DeduceResultModel
    ) -> None:
        """Update round result"""
        if step_name == "proposal":
            self.round_result.proposal = result
        elif step_name == "question":
            self.round_result.question = result
        elif step_name == "deduce":
            self.round_result.deduce = result
        else:
            raise ValueError(f"Invalid step name: {step_name}")

    def get_game_statistics(self) -> Dict[str, Any]:
        """Get complete game data"""
        return {
            "session_id": self.session_id,
            "model_name": self.generic_model_name,
            "model_provider": self.model_provider,
            "setup": self.setup.model_dump(),
            "max_rounds": self.max_rounds,
            "game_prompts": self.game_prompts.model_dump(),
            "game_state": self.game_state.model_dump(),
            "round_history": self.round_history,
            "messages": self.messages
        }
    
    def get_game_short_statistics(self) -> Dict[str, Any]:
        """Get short game statistics"""
        return {
            "session_id": self.session_id,
            "model_name": self.generic_model_name,
            "model_provider": self.model_provider,
            "setup_id": self.setup.setup_id,
            "game_state": self.game_state.model_dump(),
        }

    def save_game_to_json_with_path(self, file_path: str) -> None:
        """Save game data to file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.get_game_statistics(), f,
                      indent=4, ensure_ascii=False)

    def save_game_to_txt_with_path(self, file_path: str) -> None:
        """Save game data to file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.get_game_statistics())

    def save_game_to_json(self) -> Optional[str]:
        """Save game data to file"""
        # detect if save folder is folder or file
        if self.save_folder:
            if os.path.isdir(self.save_folder):
                file_path = os.path.join(
                    self.save_folder, f"{self.get_game_id()}.json")
                self.save_game_to_json_with_path(file_path)
                return file_path
            else:
                self.save_game_to_json_with_path(self.save_folder)
                return self.save_folder
        return None