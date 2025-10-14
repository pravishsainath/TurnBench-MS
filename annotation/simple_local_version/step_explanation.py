proposal_explanation = """Now entering the Proposal stage. During this stage, you will need to compose a 3-digit code to help you learn as much as possible from the verifiers.
BLUE = first digit(X), YELLOW = second digit(Y), PURPLE = third digit(Z).
Each digit(X, Y, Z) can be 1, 2, 3, 4, or 5 (digits may repeat).

Explain why you chose this code first, then enter your 3-digit guess code.
"""

question_explanation = """Verifier Rules:
- Each verifier checks ONE specific property (criterion) about the code.
- Each verifier has multiple potential criteria, but for each game, only ONE is secretly selected as 'active'. You don't know which criterion is active for any given verifier.
- Focus of Verification: When testing your code against a verifier, it **exclusively** evaluates it against its **single, active criterion**. The verifier completely ignores all other potential criteria, including its own inactive ones.
- PASS Condition: A verifier returns `<PASS>` **if and only if** your code satisfies this single active criterion. A `<PASS>` confirms *only* that this specific rule was met by the tested code.
- FAIL Condition: A verifier returns `<FAIL>` **if and only if** your code does not satisfy this single active criterion. A `<FAIL>` indicates *only* that this specific rule was violated by the tested code.
- Non-Overlapping Information: The active criteria selected across different verifiers for a game will provide distinct information. For example, if one active criterion establishes 'YELLOW is the smallest', no other active criterion will simply state 'YELLOW is less than BLUE'.

Now entering the Question Verifiers stage. During this stage, you will need to sequentially choose 0 to 3 verifiers to test your proposed code (but you need to ensure that your code passes all verifiers when you submit). After each selection, you will see the result, and then you can decide whether to select the next one.

For the first choice, you need to explain why you chose this verifier first.
For the following choices, you can analysis the result first, then explain why you chose this verifier.

If you want to skip, leave the choice blank and click next step.
"""

dudecode_explanation = """Now entering the Deduce stage. Based on all the information gathered, you must decide whether to submit your final answer OR continue to the next round.

You have two options:
1. Submit a Final Answer:
    - If you are confident you have deduced the single, correct 3-digit code that satisfies all the game's active verifier criteria(not only the ones you have tested), you can submit it.
    - Outcome if Correct: You immediately win the game. Your ranking will be determined based on the number of rounds played and verifiers used (fewer is better).
    - Outcome if Incorrect: This is critical! If your submitted code is incorrect, you are immediately eliminated from the game. You will not be ranked, regardless of how few rounds you played or verifiers you used. Only players who submit the correct final answer are eligible for ranking.
    - Therefore, only submit when you are highly confident in your answer. Prioritize correctness above all else.

2. Continue to Next Round:
    - If you are not yet certain about the correct code, choose this option to proceed to the next round and gather more information using the verifiers.

Explain why you chose this code or why you want to continue to the next round.
If you want to skip, leave the choice blank and click next step.
"""
