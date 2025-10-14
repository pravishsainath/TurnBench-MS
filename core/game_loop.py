import re
import time
from typing import List, Dict, Any

from core.game_session import GameSession
from llm.llm_manager import LLMClient
from verifier.verifier_manager import VerifierManager
from core.game_stage import ProposalStage, QuestionStage, DeduceStage
from utils.logger import setup_logger

class GameLoop:
    """
    Main game loop class, controlling the entire game process
    Coordinates the various stages of the game, manages the number of rounds and game end conditions
    """
    
    def __init__(
        self, 
        game_session: GameSession, 
        llm_client: LLMClient,
        verifier_manager: VerifierManager,
        log_level: int
    ) -> None:
        """Initialize the game loop"""
        self.logger = setup_logger("GameLoop", log_level)
        self.game_session = game_session
        self.llm_client = llm_client
        self.verifier_manager = verifier_manager
        
        # initialize game stages
        self.proposal_stage = ProposalStage(game_session, llm_client, verifier_manager, log_level)
        self.question_stage = QuestionStage(game_session, llm_client, verifier_manager, log_level)
        self.deduce_stage = DeduceStage(game_session, llm_client, verifier_manager, log_level)
        
        # define round structure
        self.round_structure = {
            "proposal": self.proposal_stage.execute, 
            "question": self.question_stage.execute,
            "deduce": self.deduce_stage.execute
        }

    def run(self) -> Dict[str, Any]:
        """Run the main game loop until the maximum number of rounds is reached or the game ends"""
        try:
            start_time = time.time()
            while not self.game_session.is_game_over():
                self.logger.debug(f"{self.game_session.experiment_id}: Round {self.game_session.game_state.total_rounds+1} started")
                if self.game_session.check_over_rounds():
                    self.logger.debug(f"{self.game_session.experiment_id}: Game over because of over rounds")
                    break
                self.game_session.refresh_round_result()
                self.execute_round()
                self.logger.debug(f"{self.game_session.experiment_id}: Round {self.game_session.game_state.total_rounds+1} completed")
                self.game_session.add_round_result()
                self.game_session.update_game_state_at_round_end()
            end_time = time.time()
            time_used = end_time - start_time
            self.game_session.update_game_time(time_used)
            saved_path = self.game_session.save_game_to_json()
            self.logger.debug(f"Game {self.game_session.experiment_id} {f'saved to {saved_path}' if saved_path else 'not saved'}")
            self.logger.debug(f"Game {self.game_session.experiment_id} time taken: {time_used} seconds")
        except Exception as e:
            self.logger.debug(f"{self.game_session.experiment_id}: Round {self.game_session.game_state.total_rounds+1} failed")
            raise e
            
        
    def execute_round(self) -> None:
        """Execute a game round, including proposal, question, deduce and end stages"""
        # execute each step
        for step_name, step_func in self.round_structure.items():
            self.logger.debug(f"{self.game_session.experiment_id}: {step_name} stage started")
            try:
                step_func()
                self.logger.debug(f"{self.game_session.experiment_id}: {step_name} stage completed")
            except Exception as e:
                self.logger.debug(f"{self.game_session.experiment_id}: {step_name} stage failed")
                raise Exception(f"Step: {step_name} failed, exception: {e}")
