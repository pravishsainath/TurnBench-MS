"""
question prompt templates, for question stage
"""


classic_first_question_prompt_with_hint = """You are now entering the **Verifier Questioning Stage** of this round.

**Current Verifiers**:
{verifier_descriptions}

**Stage Purpose**:
In this stage, you can test your proposed 3-digit code using verifiers. Each verifier checks one hidden criterion. Use the test results to gather information and refine your deduction.

**Verifier Rules Summary**:
- Each verifier has ONE secretly selected active criterion.
- <PASS> means your code satisfies this rule; <FAIL> means it does not.
- Active rules do NOT overlap between verifiers.

**Your Goal in This Stage**:
- Choosing verifiers is optional; testing 0 verifiers is allowed. If you want to choose the verifier, you must choose verifiers **one at a time**. After each result, you may decide whether to test another. You may choose to test 0 to 3 verifiers **in total** during this round.
- **Passing all tested verifiers does NOT mean the code is correct.** To win, your code must satisfy the hidden criterion of **all verifiers**, whether tested or not.

**What You Must Do Now**:
- If you want to choose a verifier to test your proposed code, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""


classic_first_question_prompt_with_reasoning_with_hint = """You are now entering the **Verifier Questioning Stage** of this round.

Current Verifiers:
{verifier_descriptions}

**Stage Purpose**:
In this stage, you can test your proposed 3-digit code using verifiers. Each verifier checks one hidden criterion. Use the test results to gather information and refine your deduction.

**Verifier Rules Summary**:
- Each verifier has ONE secretly selected active criterion.
- <PASS> means your code satisfies this rule; <FAIL> means it does not.
- Active rules do NOT overlap between verifiers.

**Your Goal in This Stage**:
- Choosing verifiers is optional; testing 0 verifiers is allowed. If you want to choose the verifier, you must choose verifiers **one at a time**. After each result, you may decide whether to test another. You may choose to test 0 to 3 verifiers **in total** during this round.
- **Passing all tested verifiers does NOT mean the code is correct.** To win, your code must satisfy the hidden criterion of **all verifiers**, whether tested or not.

**What You Must Do Now**:
- If you want to choose a verifier to test your proposed code, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- Explain your reasoning step by step with <REASONING> tag, then provide your choice.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing the verifier or skipping verifiers]
<CHOICE>: [your_choice]
"""





classic_following_question_prompt_with_hint = """You chose Verifier <{verifier_num}> and the result is <{verifier_result}>.

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""


classic_following_question_prompt_with_reasoning_with_hint = """You chose Verifier <{verifier_num}> and the result is <{verifier_result}>.

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- Explain your reasoning step by step based on verifier result after <REASONING> tag, then provide your choice.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing the verifier or skipping verifiers]
<CHOICE>: [your_choice]
"""





classic_after_last_question_prompt_with_hint = """You chose Verifier <{verifier_num}> and the result is <{verifier_result}>.

You have now tested the maximum number of three verifiers for this round. The next stage is the Deduce Stage. If you want to test more verifiers or new code, you can choose SKIP during the Deduce Stage to move on to the next round.
"""


classic_after_last_question_prompt_with_reasoning_with_hint = classic_after_last_question_prompt_with_hint



classic_not_valid_question_format_prompt_with_hint = """You did not follow the required response format. Please try again with same choice.

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""

classic_not_valid_question_format_prompt_with_reasoning_with_hint = """You did not follow the required response format. Please try again with same choice.

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- Explain your reasoning step by step based on verifier result after <REASONING> tag, then provide your choice.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing the verifier or skipping verifiers]
<CHOICE>: [your_choice]
"""





classic_not_valid_verifier_choice_prompt_with_hint = """You selected Verifier <{verifier_num}>, which is not a valid verifier number.

Please choose a valid verifier or SKIP to next stage.

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""



classic_not_valid_verifier_choice_prompt_with_reasoning_with_hint = """You selected Verifier <{verifier_num}>, which is not a valid verifier number.

Please choose a valid verifier or SKIP to next stage.

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- Explain your reasoning step by step based on verifier result after <REASONING> tag, then provide your choice.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing the verifier or skipping verifiers]
<CHOICE>: [your_choice]
"""







"""
# nightmare question prompt templates, for nightmare game
"""


nightmare_first_question_prompt_with_hint = """You are now entering the **Verifier Questioning Stage** of this round.

**Current Verifiers**:
{verifier_descriptions}

**Stage Purpose**:
In this stage, you can test your proposed 3-digit code using verifiers. Each verifier checks one hidden criterion. Use the test results to gather information and refine your deduction.

**Verifier Rules Summary**:
- Each verifier has ONE secretly selected active criterion.
- Each verifier shows results for a different, hidden verifier (the mapping is randomized but fixed for the entire game).
- <PASS> means your code satisfies the active criterion of the secretly mapped verifier. <FAIL> means your code does not satisfy that criterion.
- Active rules do NOT overlap between verifiers.

**Your Goal in This Stage**:
- Choosing verifiers is optional; testing 0 verifiers is allowed. If you want to choose the verifier, you must choose verifiers **one at a time**. After each result, you may decide whether to test another. You may choose to test 0 to 3 verifiers **in total** during this round.
- **Passing all tested verifiers does NOT mean the code is correct.** To win, your code must satisfy the hidden criterion of **all verifiers**, whether tested or not.

**What You Must Do Now**:
- If you want to choose a verifier to test your proposed code, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""


nightmare_first_question_prompt_with_reasoning_with_hint = """You are now entering the **Verifier Questioning Stage** of this round.

**Current Verifiers**:
{verifier_descriptions}

**Stage Purpose**:
In this stage, you can test your proposed 3-digit code using verifiers. Each verifier checks one hidden criterion. Use the test results to gather information and refine your deduction.

**Verifier Rules Summary**:
- Each verifier has ONE secretly selected active criterion.
- Each verifier shows results for a different, hidden verifier (the mapping is randomized but fixed for the entire game).
- <PASS> means your code satisfies the active criterion of the secretly mapped verifier. <FAIL> means your code does not satisfy that criterion.
- Active rules do NOT overlap between verifiers.

**Your Goal in This Stage**:
- Choosing verifiers is optional; testing 0 verifiers is allowed. If you want to choose the verifier, you must choose verifiers **one at a time**. After each result, you may decide whether to test another. You may choose to test 0 to 3 verifiers **in total** during this round.
- **Passing all tested verifiers does NOT mean the code is correct.** To win, your code must satisfy the hidden criterion of **all verifiers**, whether tested or not.

**What You Must Do Now**:
- If you want to choose a verifier to test your proposed code, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- Explain your reasoning step by step based on verifier result after <REASONING> tag, then provide your choice.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing the verifier or skipping verifiers]
<CHOICE>: [your_choice]
"""



nightmare_following_question_prompt_with_hint = """You chose Verifier <{verifier_num}> and the result is <{verifier_result}>.

**Hint**:
- `<PASS>` means your code satisfies the active criterion of the actual Verifier it is mapped to. For example, if Verifier 1 is secretly mapped to Verifier 2, then a <PASS> from Verifier 1 means your code met Verifier 2's hidden active rule.
- `<FAIL>` means your code does not satisfy the active criterion of the actual Verifier it is mapped to. 

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- DO NOT include any explanation, only follow the response format.

**Response format**:
<CHOICE>: [your_choice]
"""


nightmare_following_question_prompt_with_reasoning_with_hint = """You chose Verifier <{verifier_num}> and the result is <{verifier_result}>.

**Hint**:
- `<PASS>` means your code satisfies the active criterion of the actual Verifier it is mapped to. For example, if Verifier 1 is secretly mapped to Verifier 2, then a <PASS> from Verifier 1 means your code met Verifier 2's hidden active rule.
- `<FAIL>` means your code does not satisfy the active criterion of the actual Verifier it is mapped to. 

**What You Must Do Now**:
- If you want to choose the next verifier to test, reply with verifier_num after <CHOICE> tag, such as <CHOICE>: 1.
- If you want to skip verifier testing for this round, reply with SKIP after <CHOICE> tag, such as <CHOICE>: SKIP.
- Explain your reasoning step by step based on verifier result after <REASONING> tag, then provide your choice.

**Response format**:
<REASONING>: [Explain your reasoning step by step for choosing the verifier or skipping verifiers]
<CHOICE>: [your_choice]
"""






nightmare_after_last_question_prompt_with_hint = classic_after_last_question_prompt_with_hint
nightmare_after_last_question_prompt_with_reasoning_with_hint = nightmare_after_last_question_prompt_with_hint


nightmare_not_valid_question_format_prompt_with_hint = classic_not_valid_question_format_prompt_with_hint
nightmare_not_valid_question_format_prompt_with_reasoning_with_hint = classic_not_valid_question_format_prompt_with_reasoning_with_hint

nightmare_not_valid_verifier_choice_prompt_with_hint = classic_not_valid_verifier_choice_prompt_with_hint
nightmare_not_valid_verifier_choice_prompt_with_reasoning_with_hint = classic_not_valid_verifier_choice_prompt_with_reasoning_with_hint


