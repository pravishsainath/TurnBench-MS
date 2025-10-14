from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class UserInfo(BaseModel):
    name: Optional[str] = None
    finished_setups: List = []
    
    
class GameData(BaseModel):
    metadata: UserInfo = UserInfo()


class ProposalResultModel(BaseModel):
    guess_code: Optional[str] = None
    reasoning: Optional[str] = None


class QuestionResultModel(BaseModel):
    verifier_choice: Optional[str] = None
    verifier_result: Optional[str] = None
    reasoning: Optional[str] = None


class DeduceResultModel(BaseModel):
    submitted: Optional[bool] = None
    submitted_code: Optional[str] = None
    guess_correct: Optional[bool] = None
    reasoning: Optional[str] = None
    num_of_verifier_passed: Optional[int] = None


class RoundResultModel(BaseModel):
    proposal: ProposalResultModel = ProposalResultModel()
    question: List[QuestionResultModel] = []
    deduce: DeduceResultModel = DeduceResultModel()


class SetupMetadata(BaseModel):
    setup_id: str = ""
    verifier_ids: List[int] = []
    active_criteria_ids: List[int] = []
    answer: str = ""
    difficulty: str = ""
    mode: str = "classic"
    verifier_details: str = ""
    
class GameSession(BaseModel):
    setup_id: str
    current_round_number: int = 1
    start_time: Optional[datetime] = None
    setup_metadata: SetupMetadata = SetupMetadata()
    rounds_data: List[RoundResultModel] = []
    last_action: Optional[str] = None
    game_over_reason: Optional[str] = None
    total_elapsed_time_seconds: Optional[int] = None


