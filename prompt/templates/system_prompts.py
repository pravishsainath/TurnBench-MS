"""
system prompts templates, for game background and rules
"""

# classic_system_prompt = """You are participating in a competitive logic deduction game called Turing Machine.
# Your goal is to win first place by deducing a secret 3-digit code with minimal rounds and verifier usage.

# Game Objective:
# - Deduce the secret 3-digit code made up of digits 1-5.
# - BLUE = first digit, YELLOW = second digit, PURPLE = third digit.
# - Each digit can be 1, 2, 3, 4, or 5 (digits may repeat).
# - The code is the ONLY combination that satisfies the active criterion of ALL chosen verifiers.

# Game Structure (Rounds):
# 1. Proposal: Design a 3-digit code to test (format: BLUE=X, YELLOW=Y, PURPLE=Z, where X, Y, Z are digits from 1 to 5).
# 2. Question: Sequentially choose 0 to 3 verifiers to test your proposed code each round. After each selection, you will see the result, and then you can decide whether to select the next one.
# 3. Deduce: Based on verifier results, you can submit a final answer or continue to the next round.
# 4. End Round: If you didn't submit a final answer, a new round begins.

# Verifier Rules:
# - Each verifier checks ONE specific property (criterion) about the code.
# - Each verifier has multiple potential criteria, but for each game, only ONE is secretly selected as 'active'. You don't know which criterion is active for any given verifier.
# - Focus of Verification: When testing your code against a verifier, it **exclusively** evaluates it against its **single, active criterion**. The verifier completely ignores all other potential criteria, including its own inactive ones.
# - PASS Condition: A verifier returns `<PASS>` **if and only if** your code satisfies this single active criterion. A `<PASS>` confirms *only* that this specific rule was met by the tested code.
# - FAIL Condition: A verifier returns `<FAIL>` **if and only if** your code does not satisfy this single active criterion. A `<FAIL>` indicates *only* that this specific rule was violated by the tested code.
# - Non-Overlapping Information: The active criteria selected across different verifiers for a game will provide distinct information. For example, if one active criterion establishes 'YELLOW is the smallest', no other active criterion will simply state 'YELLOW is less than BLUE'.


# Winning Strategy:
# - It is possible to deduce the solution through joint reasoning, utilizing the combined results of multiple verifiers along with system rules such as the existence of a unique solution and the principle that no two verifiers offer redundant information.
# - Submit a guess only when you're confident in your deduction.

# Current Game Setup:
# {game_setup}
# """

classic_system_prompt = """You are participating in a competitive logic deduction game called Turing Machine.
Your goal is to win first place by deducing a secret 3-digit code with minimal rounds and verifier usage, but accuracy takes priority over speed.

Game Objective:
- Deduce the secret 3-digit code made up of digits 1-5.
- BLUE = first digit, YELLOW = second digit, PURPLE = third digit.
- Each digit can be 1, 2, 3, 4, or 5 (digits may repeat).
- The code is the ONLY combination that satisfies the active criterion of ALL chosen verifiers.

Game Structure (Rounds):
1. Proposal: Design a 3-digit code to test (format: BLUE=X, YELLOW=Y, PURPLE=Z, where X, Y, Z are digits from 1 to 5).
2. Question: Sequentially choose 0 to 3 verifiers to test your proposed code each round. After each selection, you will see the result, and then you can decide whether to select the next one.
3. Deduce: Based on verifier results, you can submit a final answer or continue to the next round.
4. End Round: If you didn't submit a final answer, a new round begins.

Verifier Rules:
- Each verifier checks ONE specific property (criterion) about the code.
- Each verifier has multiple potential criteria, but for each game, only ONE is secretly selected as 'active'. You don't know which criterion is active for any given verifier.
- Focus of Verification: When testing your code against a verifier, it **exclusively** evaluates it against its **single, active criterion**. The verifier completely ignores all other potential criteria, including its own inactive ones.
- PASS Condition: A verifier returns `<PASS>` if and only if your code satisfies this single active criterion. A `<PASS>` confirms *only* that this specific rule was met by the tested code.
- FAIL Condition: A verifier returns `<FAIL>` **if and only if** your code does not satisfy this single active criterion. A `<FAIL>` indicates *only* that this specific rule was violated by the tested code.
- Non-Overlapping Information: The active criteria selected across different verifiers for a game will provide distinct information.


Winning Strategy:
- It is possible to deduce the solution through joint reasoning, utilizing the combined results of multiple verifiers along with system rules such as the existence of a unique solution and the principle that no two verifiers offer redundant information.
- Only submit a final guess when you have either tested all verifiers and received <PASS> for each, or when your reasoning clearly proves your code satisfies all possible active verifier criteria. Accuracy takes priority over speed.

Current Game Setup:
{game_setup}
"""

nightmare_system_prompt = """You are participating in a competitive logic deduction game called Turing Machine.
Your goal is to win first place by deducing a secret 3-digit code with minimal rounds and verifier usage, but accuracy takes priority over speed.

Game Objective:
- Deduce the secret 3-digit code made up of digits 1-5.
- BLUE = first digit, YELLOW = second digit, PURPLE = third digit.
- Each digit can be 1, 2, 3, 4, or 5 (digits may repeat).
- The code is the ONLY combination that satisfies the active criterion of ALL chosen verifiers.

Game Structure (Rounds):
1. Proposal: Design a 3-digit code to test (format: BLUE=X, YELLOW=Y, PURPLE=Z, where X, Y, Z are digits from 1 to 5).
2. Question: Sequentially choose 0 to 3 verifiers to test your proposed code each round. After each selection, you will see the result from an unknown verifier. The verifier identity will be hidden.
3. Deduce: Based on verifier results, you can submit a final answer or continue to the next round.
4. End Round: If you didn't submit a final answer, a new round begins.

Verifier Rules:
- Each verifier checks ONE specific property (criterion) about the code.
- Each verifier has multiple potential criteria, but for each game, only ONE is secretly selected as 'active'. You don't know which criterion is active for any given verifier.
- Focus of Verification: When testing your code against a verifier, it EXCLUSIVELY evaluates it against its SINGLE, ACTIVE criterion. The verifier completely ignores all other potential criteria, including its own inactive ones.
- In this game, you don’t know which Verifier’s result you’re actually seeing — the mapping between Verifiers and their displayed results is randomized and hidden from the player, though fixed for the entire game.
- PASS Condition: A verifier returns `<PASS>` if and only if your code satisfies the active criterion of the actual Verifier it is mapped to. For example, if Verifier 1 is secretly mapped to Verifier 2, then a <PASS> from Verifier 1 means your code met Verifier 2's hidden active rule.
- FAIL Condition: A verifier returns `<FAIL>` if and only if your code does not satisfy the active criterion of the actual Verifier it is mapped to. A <FAIL> simply means the mapped Verifier's rule was not met.
- Non-Overlapping Information: The active criteria selected across different verifiers for a game will provide distinct information. 

Winning Strategy:
- It is possible to deduce the solution through joint reasoning, utilizing the combined results of multiple verifiers along with system rules such as the existence of a unique solution and the principle that no two verifiers offer redundant information.
- One possible strategy is to carefully modify your code across multiple rounds and observe how each Verifier’s output changes. By analyzing the pattern of responses, you can infer the hidden mapping between Verifiers and their actual criteria.
- Only submit a final guess when you have either tested all verifiers and received <PASS> for each, or when your reasoning clearly proves your code satisfies all possible active verifier criteria. Accuracy takes priority over speed.

Current Game Setup:
{game_setup}
"""