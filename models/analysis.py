from typing import Dict, List, Optional, Any

import numpy as np
from pydantic import BaseModel, Field

from models.game import GameSetupModel, GameStateModel

class AnalysisMetadataModel(GameSetupModel, GameStateModel):
    """metadata model for game analysis"""
    model_name: str
    num_of_verifiers: int
    num_of_chat_rounds: int

class GameMetricsListDataModel(BaseModel):
    """list data model for game analysis metrics"""
    verifier_pass_rates: List[float] = Field(default_factory=list)
    used_times: List[float] = Field(default_factory=list)

    used_num_of_rounds: List[int] = Field(default_factory=list)
    used_num_of_verifiers: List[int] = Field(default_factory=list)
    used_num_of_chat_rounds: List[int] = Field(default_factory=list)
    
    used_input_tokens: List[int] = Field(default_factory=list)
    used_output_tokens: List[int] = Field(default_factory=list)
    used_reasoning_tokens: List[int] = Field(default_factory=list)

    total_response_with_formatting_error: List[int] = Field(default_factory=list)
    total_response_with_not_valid_error: List[int] = Field(default_factory=list)

    num_of_repeated_guesses: List[int] = Field(default_factory=list)
    num_of_repeated_verifier_choice_after_pass: List[int] = Field(default_factory=list)
    repeated_guess_rates: List[float] = Field(default_factory=list)
    repeated_verifier_choice_after_pass_rates: List[float] = Field(default_factory=list)

class GameMetricsStatesDataModel(BaseModel):
    """states data model for game analysis metrics"""
    num_of_games: int = 0

    average_verifier_pass_rate: float = 0
    max_used_time_for_one_game: float = 0
    average_used_time: float = 0
    
    max_used_num_of_rounds_for_one_game: int = 0
    max_used_num_of_verifiers_for_one_game: int = 0
    max_used_num_of_chat_rounds_for_one_game: int = 0
    average_used_num_of_rounds: float = 0
    average_used_num_of_verifiers: float = 0
    average_used_num_of_chat_rounds: float = 0

    max_input_tokens_for_one_game: int = 0
    max_output_tokens_for_one_game: int = 0
    max_reasoning_tokens_for_one_game: int = 0
    average_input_tokens: float = 0
    average_output_tokens: float = 0
    average_reasoning_tokens: float = 0

    max_num_of_response_with_formatting_error_for_one_game: int = 0
    max_num_of_response_with_not_valid_error_for_one_game: int = 0
    average_num_of_response_with_formatting_error: float = 0
    average_num_of_response_with_not_valid_error: float = 0
    num_of_games_with_response_with_formatting_error: int = 0
    num_of_games_with_response_with_not_valid_error: int = 0

    max_num_of_repeated_guesses_for_one_game: int = 0
    max_num_of_repeated_verifier_choice_after_pass_for_one_game: int = 0
    max_repeated_guess_rate_for_one_game: float = 0
    max_repeated_verifier_choice_after_pass_rate_for_one_game: float = 0
    average_num_of_repeated_guesses: float = 0
    average_num_of_repeated_verifier_choice_after_pass: float = 0
    average_repeated_guess_rate: float = 0
    average_repeated_verifier_choice_after_pass_rate: float = 0
    num_of_games_with_repeated_guesses: int = 0
    num_of_games_with_repeated_verifier_choice_after_pass: int = 0

class GameMetricsModel(GameMetricsListDataModel, GameMetricsStatesDataModel):
    """base model for storing game analysis metrics"""

    # distribution data
    used_num_of_rounds_distribution: Dict[int, int] = Field(default_factory=dict)
    used_num_of_verifiers_distribution: Dict[int, int] = Field(default_factory=dict)
    used_num_of_chat_rounds_distribution: Dict[int, int] = Field(default_factory=dict)
    formatting_error_distribution: Dict[int, int] = Field(default_factory=dict)
    not_valid_error_distribution: Dict[int, int] = Field(default_factory=dict)
    repeated_guesses_distribution: Dict[int, int] = Field(default_factory=dict)
    repeated_verifier_choice_distribution: Dict[int, int] = Field(default_factory=dict)

    def calculate_distributions(self, list_data: List[int]) -> Dict[int, int]:
        """calculate distributions for the list data"""
        distribution = {}
        for item in list_data:
            if item not in distribution:
                distribution[item] = 1
            else:
                distribution[item] += 1
        return distribution
        
    def build_states_data(self) -> None:
        if len(self.used_num_of_rounds) == 0:
            return
        self.num_of_games = len(self.used_num_of_rounds)
        self.average_verifier_pass_rate = np.mean(self.verifier_pass_rates)
        self.max_used_time_for_one_game = max(self.used_times)
        self.average_used_time = np.mean(self.used_times)
        self.max_used_num_of_rounds_for_one_game = max(self.used_num_of_rounds)
        self.max_used_num_of_verifiers_for_one_game = max(self.used_num_of_verifiers)
        self.max_used_num_of_chat_rounds_for_one_game = max(self.used_num_of_chat_rounds)
        self.average_used_num_of_rounds = np.mean(self.used_num_of_rounds)
        self.average_used_num_of_verifiers = np.mean(self.used_num_of_verifiers)
        self.average_used_num_of_chat_rounds = np.mean(self.used_num_of_chat_rounds)
        self.max_input_tokens_for_one_game = max(self.used_input_tokens)
        self.max_output_tokens_for_one_game = max(self.used_output_tokens)
        self.max_reasoning_tokens_for_one_game = max(self.used_reasoning_tokens)
        self.average_input_tokens = np.mean(self.used_input_tokens)
        self.average_output_tokens = np.mean(self.used_output_tokens)
        self.average_reasoning_tokens = np.mean(self.used_reasoning_tokens)
        self.max_num_of_response_with_formatting_error_for_one_game = max(self.total_response_with_formatting_error)
        self.max_num_of_response_with_not_valid_error_for_one_game = max(self.total_response_with_not_valid_error)
        self.average_num_of_response_with_formatting_error = np.mean(self.total_response_with_formatting_error)
        self.average_num_of_response_with_not_valid_error = np.mean(self.total_response_with_not_valid_error)
        self.num_of_games_with_response_with_formatting_error = sum([1 if x > 0 else 0 for x in self.total_response_with_formatting_error])
        self.num_of_games_with_response_with_not_valid_error = sum([1 if x > 0 else 0 for x in self.total_response_with_not_valid_error])
        self.max_num_of_repeated_guesses_for_one_game = max(self.num_of_repeated_guesses)
        self.max_num_of_repeated_verifier_choice_after_pass_for_one_game = max(self.num_of_repeated_verifier_choice_after_pass)
        self.max_repeated_guess_rate_for_one_game = max(self.repeated_guess_rates)
        self.max_repeated_verifier_choice_after_pass_rate_for_one_game = max(self.repeated_verifier_choice_after_pass_rates)
        self.average_num_of_repeated_guesses = np.mean(self.num_of_repeated_guesses)
        self.average_num_of_repeated_verifier_choice_after_pass = np.mean(self.num_of_repeated_verifier_choice_after_pass)
        self.average_repeated_guess_rate = np.mean(self.repeated_guess_rates)
        self.average_repeated_verifier_choice_after_pass_rate = np.mean(self.repeated_verifier_choice_after_pass_rates)
        self.num_of_games_with_repeated_guesses = sum([1 if x > 0 else 0 for x in self.num_of_repeated_guesses])
        self.num_of_games_with_repeated_verifier_choice_after_pass = sum([1 if x > 0 else 0 for x in self.num_of_repeated_verifier_choice_after_pass])
        self.formatting_error_distribution = self.calculate_distributions(self.total_response_with_formatting_error)
        self.not_valid_error_distribution = self.calculate_distributions(self.total_response_with_not_valid_error)
        self.repeated_guesses_distribution = self.calculate_distributions(self.num_of_repeated_guesses)
        self.repeated_verifier_choice_distribution = self.calculate_distributions(self.num_of_repeated_verifier_choice_after_pass)
        self.used_num_of_rounds_distribution = self.calculate_distributions(self.used_num_of_rounds)
        self.used_num_of_verifiers_distribution = self.calculate_distributions(self.used_num_of_verifiers)
        self.used_num_of_chat_rounds_distribution = self.calculate_distributions(self.used_num_of_chat_rounds)
    

class AnalysisResultModel(BaseModel):
    """game analysis result model"""
    num_of_games: int = 0
    longest_context_length: int = 0
    game_over_reason_count: Dict[str, int] = Field(default_factory=dict)
    average_used_num_of_rounds: float = 0
    average_used_num_of_verifiers: float = 0
    average_used_num_of_chat_rounds: float = 0
    success_games: GameMetricsModel = Field(default_factory=GameMetricsModel)
    fail_games: GameMetricsModel = Field(default_factory=GameMetricsModel)
    
    # distribution data for both success and fail games
    formatting_error_distribution: Dict[int, int] = Field(default_factory=dict)
    not_valid_error_distribution: Dict[int, int] = Field(default_factory=dict)
    repeated_guesses_distribution: Dict[int, int] = Field(default_factory=dict)
    repeated_verifier_choice_distribution: Dict[int, int] = Field(default_factory=dict)
    used_num_of_rounds_distribution: Dict[int, int] = Field(default_factory=dict)
    used_num_of_verifiers_distribution: Dict[int, int] = Field(default_factory=dict)
    used_num_of_chat_rounds_distribution: Dict[int, int] = Field(default_factory=dict)
    
    def merge_dictionaries(self, dict1: Dict[int, int], dict2: Dict[int, int]) -> None:
        for key, value in dict2.items():
            if key in dict1:
                dict1[key] += value
            else:
                dict1[key] = value
    
    def build_average_data(self) -> None:
        """build average data for both success and fail games"""
        all_used_num_of_rounds = self.success_games.used_num_of_rounds+self.fail_games.used_num_of_rounds
        if len(all_used_num_of_rounds) == 0:
            return
        self.average_used_num_of_rounds = np.mean(all_used_num_of_rounds)
        self.average_used_num_of_verifiers = np.mean(self.success_games.used_num_of_verifiers+self.fail_games.used_num_of_verifiers)
        self.average_used_num_of_chat_rounds = np.mean(self.success_games.used_num_of_chat_rounds+self.fail_games.used_num_of_chat_rounds)
        
    def build_distribution_data(self) -> None:
        """build distribution data for both success and fail games"""
        # merge data from success and fail games
        s = self.success_games
        f = self.fail_games
        
        # merge dictionaries correctly, create new dictionaries without modifying original ones
        self.formatting_error_distribution = {**s.formatting_error_distribution}
        self.merge_dictionaries(self.formatting_error_distribution, f.formatting_error_distribution)
                
        self.not_valid_error_distribution = {**s.not_valid_error_distribution}
        self.merge_dictionaries(self.not_valid_error_distribution, f.not_valid_error_distribution)
        
        self.repeated_guesses_distribution = {**s.repeated_guesses_distribution}
        self.merge_dictionaries(self.repeated_guesses_distribution, f.repeated_guesses_distribution)
        
        self.repeated_verifier_choice_distribution = {**s.repeated_verifier_choice_distribution}
        self.merge_dictionaries(self.repeated_verifier_choice_distribution, f.repeated_verifier_choice_distribution)

        self.used_num_of_rounds_distribution = {**s.used_num_of_rounds_distribution}
        self.merge_dictionaries(self.used_num_of_rounds_distribution, f.used_num_of_rounds_distribution)

        self.used_num_of_verifiers_distribution = {**s.used_num_of_verifiers_distribution}
        self.merge_dictionaries(self.used_num_of_verifiers_distribution, f.used_num_of_verifiers_distribution)

        self.used_num_of_chat_rounds_distribution = {**s.used_num_of_chat_rounds_distribution}
        self.merge_dictionaries(self.used_num_of_chat_rounds_distribution, f.used_num_of_chat_rounds_distribution)
