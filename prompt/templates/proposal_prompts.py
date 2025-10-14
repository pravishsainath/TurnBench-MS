"""
proposal prompt templates, for proposal stage
"""


classic_proposal_prompt_with_hint = """You are now entering the **Proposal Stage** of this round.

**Stage Purpose**:
In this stage, you need to compose a 3-digit code to help you to gather information from the verifiers. The code can NOT be changed in the subsequent stages of this round.

**3-digit code rules**:
- BLUE = first digit (X), YELLOW = second digit (Y), PURPLE = third digit (Z).  
- Each digit (X, Y, Z) can be 1, 2, 3, 4, or 5. Digits may repeat.

**Your Goal in This Stage**:
- Design a code that will test a specific hypothesis.
- Think about what a <PASS> or <FAIL> would tell you.
- Choose a code that lets you learn something meaningful from verifiers.

**What You Must Do Now**:
- Reply the code you want to use in this round with required response format. For example, <CHOICE>: BLUE=1, YELLOW=1, PURPLE=1
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: BLUE=X, YELLOW=Y, PURPLE=Z
"""


classic_proposal_prompt_with_reasoning_with_hint = """You are now entering the **Proposal Stage** of this round.

**Stage Purpose**:
In this stage, you need to compose a 3-digit code to help you to gather information from the verifiers. The code can NOT be changed in the subsequent stages of this round.

**3-digit code rules**:
- BLUE = first digit (X), YELLOW = second digit (Y), PURPLE = third digit (Z).  
- Each digit (X, Y, Z) can be 1, 2, 3, 4, or 5. Digits may repeat.

**Your Goal in This Stage**:
- Design a code that will test a specific hypothesis.
- Think about what a <PASS> or <FAIL> would tell you.
- Choose a code that lets you learn something meaningful from verifiers.

**What You Must Do Now**:
- Reply the code you want to use in this round with required response format. For example, <PROPOSAL>: BLUE=1, YELLOW=1, PURPLE=1
- Explain your reasoning step by step with <REASONING> tag, then provide your code.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing this code]
<CHOICE>: BLUE=[X], YELLOW=[Y], PURPLE=[Z]
"""


classic_not_valid_proposal_format_prompt_with_hint = """You did not follow the required response format. Please try again with same code.

**What You Must Do Now**:
- Reply the code you want to use in this round with required response format. For example, <PROPOSAL>: BLUE=1, YELLOW=1, PURPLE=1
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: BLUE=[X], YELLOW=[Y], PURPLE=[Z]
"""

classic_not_valid_proposal_format_prompt_with_reasoning_with_hint = """You did not follow the required response format. Please try again with same code.

**What You Must Do Now**:
- Reply the code you want to use in this round with required response format. For example, <PROPOSAL>: BLUE=1, YELLOW=1, PURPLE=1
- Explain your reasoning step by step with <REASONING> tag, then provide your code.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing this code]
<CHOICE>: BLUE=[X], YELLOW=[Y], PURPLE=[Z]
"""








nightmare_proposal_prompt_with_hint = """You are now entering the **Proposal Stage** of this round.

**Stage Purpose**:
In this stage, you need to compose a 3-digit code to help you to gather information from the verifiers. The code can NOT be changed in the subsequent stages of this round.

**3-digit code rules**:
- BLUE = first digit (X), YELLOW = second digit (Y), PURPLE = third digit (Z).  
- Each digit (X, Y, Z) can be 1, 2, 3, 4, or 5. Digits may repeat.

**Your Goal in This Stage**:
- Design a code that will test a specific hypothesis.
- Think about what a <PASS> or <FAIL> would tell you, but you don’t know which Verifier’s result you’re actually seeing — the mapping between Verifiers and their displayed results is randomized and hidden from the player, though fixed for the entire game.
- Choose a code that lets you learn something meaningful from verifiers.

**What You Must Do Now**:
- Reply the code you want to use in this round with required response format. For example, <CHOICE>: BLUE=1, YELLOW=1, PURPLE=1
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: BLUE=X, YELLOW=Y, PURPLE=Z
"""


nightmare_proposal_prompt_with_reasoning_with_hint = """You are now entering the **Proposal Stage** of this round.

**Stage Purpose**:
In this stage, you need to compose a 3-digit code to help you to gather information from the verifiers. The code cannot be changed in the subsequent stages of this round.

**3-digit code rules**:
- BLUE = first digit (X), YELLOW = second digit (Y), PURPLE = third digit (Z).  
- Each digit (X, Y, Z) can be 1, 2, 3, 4, or 5. Digits may repeat.

**Your Goal in This Stage**:
- Design a code that will test a specific hypothesis.
- Think about what a <PASS> or <FAIL> would tell you, but you don’t know which Verifier’s result you’re actually seeing — the mapping between Verifiers and their displayed results is randomized and hidden from the player, though fixed for the entire game.
- Choose a code that lets you learn something meaningful from verifiers.

**What You Must Do Now**:
- Reply the code you want to use in this round with required response format. For example, <PROPOSAL>: BLUE=1, YELLOW=1, PURPLE=1
- Explain your reasoning step by step with <REASONING> tag, then provide your code.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing this code]
<CHOICE>: BLUE=[X], YELLOW=[Y], PURPLE=[Z]
"""


nightmare_not_valid_proposal_format_prompt_with_hint = classic_not_valid_proposal_format_prompt_with_hint

nightmare_not_valid_proposal_format_prompt_with_reasoning_with_hint = classic_not_valid_proposal_format_prompt_with_reasoning_with_hint


