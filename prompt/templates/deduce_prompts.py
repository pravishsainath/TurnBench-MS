"""
deduce prompts templates, for deduce stage
"""

classic_deduce_prompt_with_hint = """You are now entering the **Deduce Stage** of this round.

**Stage Purpose**:
In this stage, you can analyze all the information gathered then decide whether to continue to the next round or submit a final guess.

**Hint**:
- Passing all tested verifiers does not mean the code is correct if not all verifiers were tested. To be correct, the code must satisfy the hidden criteria of all verifiers, not just the ones you tested.
- You may choose not to test some verifiers if you can clearly reason that your code meets their requirements. But you must ensure every verifier is either tested and passed, or clearly justified through reasoning. Testing and passing only part of the verifiers is not enough if others are ignored.
- This stage **is not for testing**, you don't have to submit an answer; you can proceed to the next round to continue gathering information.
- Accuracy takes priority over speed. If you submit, the game will end, and an incorrect guess will result in immediate failure.

**Your Goal in This Stage**:
- Decide whether to submit the final guess or continue to the next round. Submit the final guess will end the game, continue to the next round will help you gather more information.
- Submission is not mandatory, you must make this decision based on your own reasoning.

**What You Must Do Now**:
- If you want to continue to the next round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP
- If you want to submit a final guess to end the game, reply with BLUE=X, YELLOW=Y, PURPLE=Z after <CHOICE> tag, such as <CHOICE>: BLUE=1, YELLOW=1, PURPLE=1.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""

classic_deduce_prompt_with_reasoning_with_hint = """You are now entering the **Deduce Stage** of this round.

**Stage Purpose**:
In this stage, you can analyze all the information gathered then decide whether to submit a final guess or continue to the next round.

**Hint**:
- Passing all tested verifiers does not mean the code is correct if not all verifiers were tested. To be correct, the code must satisfy the hidden criteria of all verifiers, not just the ones you tested.
- You may choose not to test some verifiers if you can clearly reason that your code meets their requirements. But you must ensure every verifier is either tested and passed, or clearly justified through reasoning. Testing and passing only part of the verifiers is not enough if others are ignored.
- This stage **is not for testing**, you don't have to submit an answer; you can proceed to the next round to continue gathering information.
- Accuracy takes priority over speed. If you submit, the game will end, and an incorrect guess will result in immediate failure.

**Your Goal in This Stage**:
- Analysis all information gathered.
- Decide whether to submit the final guess or continue to the next round.
- Submission is not mandatory, you must make this decision based on your own reasoning.

**What You Must Do Now**:
- If you want to continue to the next round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP
- If you want to submit a final guess to end the game, reply with BLUE=X, YELLOW=Y, PURPLE=Z after <CHOICE> tag, such as <CHOICE>: BLUE=1, YELLOW=1, PURPLE=1.
- Explain your reasoning step by step with <REASONING> tag, then provide your choice. If you want to submit a final guess, you must provide the reasons for not proceeding to the next round.

**Response format**:
<REASONING>: [Analysis and explain your reasoning step by step for continue to next round or submit final guess]
<CHOICE>: [your_choice]
"""



classic_deduce_result_prompt_with_hint = "The final guess is {submitted_code}. The answer is {answer}, the guess is {is_correct}."
classic_deduce_result_prompt_with_reasoning_with_hint = classic_deduce_result_prompt_with_hint




classic_not_valid_deduce_format_prompt_with_hint = """You did NOT follow the response format. Please try again.

**What You Must Do Now**:
- If you want to continue to the next round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP
- If you want to submit a final guess to end the game, reply with BLUE=X, YELLOW=Y, PURPLE=Z after <CHOICE> tag, such as <CHOICE>: BLUE=1, YELLOW=1, PURPLE=1.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""


classic_not_valid_deduce_format_prompt_with_reasoning_with_hint = """You did NOT follow the response format. Please try again.

**What You Must Do Now**:
- If you want to continue to the next round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP
- If you want to submit a final guess to end the game, reply with BLUE=X, YELLOW=Y, PURPLE=Z after <CHOICE> tag, such as <CHOICE>: BLUE=1, YELLOW=1, PURPLE=1.
- Explain your reasoning step by step with <REASONING> tag, then provide your choice.

**Response format**:
<REASONING>: [Analysis and explain your reasoning step by step for submitting the final guess or continue to next round]
<CHOICE>: [your_choice]
"""



nightmare_deduce_prompt_with_hint = classic_deduce_prompt_with_hint
nightmare_deduce_prompt_with_reasoning_with_hint = classic_deduce_prompt_with_reasoning_with_hint

nightmare_deduce_result_prompt_with_hint = classic_deduce_result_prompt_with_hint
nightmare_deduce_result_prompt_with_reasoning_with_hint = classic_deduce_result_prompt_with_reasoning_with_hint

nightmare_not_valid_deduce_format_prompt_with_hint = classic_not_valid_deduce_format_prompt_with_hint
nightmare_not_valid_deduce_format_prompt_with_reasoning_with_hint = classic_not_valid_deduce_format_prompt_with_reasoning_with_hint




