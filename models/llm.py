from typing import Dict, Any, Optional
from pydantic import BaseModel

class LLMResponseUsageModel(BaseModel):
    input_tokens: int
    output_tokens: int
    reasoning_tokens: Optional[int] = None
    prompt_cache_hit_tokens: Optional[int] = None
    cost: Optional[float] = None

class LLMResponseModel(LLMResponseUsageModel):
    content: str
    model_level_reasoning_content: Optional[str] = None
    service_provider: Optional[str] = None
