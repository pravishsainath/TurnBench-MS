from typing import Optional, List, Tuple

from pydantic import BaseModel

class GameSetupModel(BaseModel):
    setup_id: str
    answer: str
    verifier_ids: List[int]
    active_criteria_ids: List[int]
    nightmare_verifier_ids: Optional[List[int]] = None
    nightmare_active_criteria_ids: Optional[List[int]] = None
    difficulty: str

class ProposalResultModel(BaseModel):
    guess_code: str = ""
    reasoning: Optional[str] = None
    model_reasoning: Optional[str] = None

class QuestionResultModel(BaseModel):
    verifier_choice: Optional[str] = None
    verifier_result: Optional[str] = None
    reasoning: Optional[str] = None
    model_reasoning: Optional[str] = None

class DeduceResultModel(BaseModel):
    submitted: bool = False
    submitted_code: Optional[str] = None
    guess_correct: Optional[bool] = None
    reasoning: Optional[str] = None
    model_reasoning: Optional[str] = None
    num_of_verifier_passed: Optional[int] = None

class RoundResultModel(BaseModel):
    proposal: ProposalResultModel = ProposalResultModel()
    question: List[QuestionResultModel] = []
    deduce: DeduceResultModel = DeduceResultModel()

class GameStateModel(BaseModel):
    total_rounds: int = 0
    verifier_uses_total: int = 0
    game_over: bool = False
    game_over_reason: Optional[str] = None
    submitted_code: Optional[str] = None
    success: bool = False
    num_of_verifier_passed: Optional[int] = None
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_prompt_cache_hit_tokens: int = 0
    total_reasoning_tokens: int = 0
    total_response_with_formatting_error: int = 0
    total_response_with_not_valid_error: int = 0
    longest_context_length: int = 0
    with_reasoning: bool = True
    with_hint: bool = True
    mode: str = "classic"
    total_time: float = 0
    all_guesses: List[str] = []
    all_verifier_choices: List[List[Tuple[str, str]]] = []