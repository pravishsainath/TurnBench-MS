import itertools
from typing import Dict, Any, List, Tuple

from verifier.verifier_manager import VerifierManager
from core.game_setup_manager import GameSetupManager
from models.game import GameSetupModel

def get_all_possible_codes() -> List[str]:
    all_codes = []
    for blue in range(1,6):
        for yellow in range(1,6):
            for purple in range(1,6):
                all_codes.append(f"{blue}{yellow}{purple}")
    return all_codes

all_possible_codes = get_all_possible_codes()

def get_possible_criteria_ids(
    verifier_manager: VerifierManager, 
    all_combinations: List[Tuple[Tuple[str, int], ...]],
    answer: str
) -> List[str]:
    possible_combination = []
    for combination in all_combinations:
        possible_codes_for_current_combination = []
        for code in all_possible_codes:
            passed_all_criteria = True
            for verifier_id, criterion_index in combination:
                if not verifier_manager.verify(verifier_id, code, criterion_index):
                    passed_all_criteria = False
                    break
            if passed_all_criteria:
                possible_codes_for_current_combination.append(code)
        if len(possible_codes_for_current_combination) == 1:
            if possible_codes_for_current_combination[0] == answer:
                possible_combination.append(combination)
    if len(possible_combination) == 0:
        return None
    return possible_combination

def get_all_combinations(verifier_ids: List[str], possible_criteria_ids: Dict[str, List[int]]) -> List[Tuple[Tuple[str, int], ...]]:
    """Generates all possible combinations of activated criteria based on the possible criteria for each verifier."""
    if not verifier_ids:
        return []

    # Create a list of iterables, where each iterable contains (verifier_id, criterion_index) pairs for one verifier
    choices_per_verifier = []
    for vid in verifier_ids:
        criteria_indices = possible_criteria_ids.get(vid, [])
        # If any verifier has no possible criteria, the total number of combinations is zero.
        if not criteria_indices:
            return []
        choices_per_verifier.append([(vid, index) for index in criteria_indices])

    # Calculate the Cartesian product
    all_combinations_iterator = itertools.product(*choices_per_verifier)

    # Convert the iterator to a list of tuples
    return list(all_combinations_iterator)

def auto_detect_actived_criteria(setup: GameSetupModel, verifier_manager: VerifierManager, more_than_one_possible_combination_counter: int) -> List[str]:
    """Auto detect the actived criteria from the game setup."""
    active_criteria_ids = []

    possible_criteria_ids = {}
    answer = setup.answer
    verifiers = verifier_manager.get_verifiers_by_ids(setup.verifier_ids)
    for vid, verifier in verifiers.items():
        for i, criterion in enumerate(verifier.criteria):
            verify_result = criterion["func"](answer)
            if verify_result:
                if vid not in possible_criteria_ids:
                    possible_criteria_ids[vid] = []
                possible_criteria_ids[vid].append(i)
        if vid not in possible_criteria_ids:
            print(f"Warning: No possible criteria for verifier {vid}")
    if sum(len(criteria_ids) for criteria_ids in possible_criteria_ids.values()) > len(verifiers):
        all_possible_combinations = get_all_combinations(setup.verifier_ids, possible_criteria_ids)
        possible_combination_after_verification = get_possible_criteria_ids(verifier_manager, all_possible_combinations, answer)
        if possible_combination_after_verification is None:
            print(setup.setup_id)
        if len(possible_combination_after_verification) > 1:
            print(f"Warning: More than one possible combination after verification for setup {setup.setup_id}")
            for combination in possible_combination_after_verification:
                for vid, criterion_index in combination:
                    criterion = verifier_manager.get_criterion_by_verifier_id_and_criterion_index(vid, criterion_index)
                    print(f"Verifier {vid}, Criterion {criterion_index}: {criterion['description']}")
                print("")
            print("warning: will choose the last one")
            more_than_one_possible_combination_counter += 1
            for vid in setup.verifier_ids:
                possible_combination_dict = dict(possible_combination_after_verification[-1])
                active_criteria_ids.append(possible_combination_dict[vid])
        elif len(possible_combination_after_verification) == 1:
            possible_combination_dict = dict(possible_combination_after_verification[0])
            for vid in setup.verifier_ids:
                active_criteria_ids.append(possible_combination_dict[vid])
        else:
            print(f"Warning: No possible combination after verification for setup {setup.setup_id}")
            for vid in setup.verifier_ids:
                active_criteria_ids.append(-1)
    else:
        for vid in setup.verifier_ids:
            active_criteria_ids.append(possible_criteria_ids[vid][0])

    return active_criteria_ids, more_than_one_possible_combination_counter

def single_game_setup_test(setup_id: str = "A41AA5"):
    game_setup_path = "data/configs/game_setups.json"
    verifier_config_path = "data/configs/verifiers_test.json"
    more_than_one_possible_combination_counter = 0

    game_setup_manager = GameSetupManager.from_json(game_setup_path)
    verifier_manager = VerifierManager()
    verifier_manager.load_verifiers_from_config(verifier_config_path)
    detected_active_criteria_ids, more_than_one_possible_combination_counter = auto_detect_actived_criteria(game_setup_manager.load_setup(setup_id), verifier_manager, more_than_one_possible_combination_counter)
    game_setup_manager.set_active_criteria_ids_by_setup_id(setup_id, detected_active_criteria_ids)
    print(f"Setup {setup_id} detected active criteria ids: {detected_active_criteria_ids}")
    game_setup_manager.to_json(game_setup_path)

def multiple_game_setup_test():
    # game_setup_path = "data/configs/game_setups_meta_data.json"
    game_setup_path = "data/configs/game_setups_30_easy_meta_data.json"
    # game_setup_path_new = "data/configs/game_setups_new_auto_detected.json"
    game_setup_path_new = "data/configs/game_setups_30_easy_meta_data_auto_detected.json"
    verifier_config_path = "data/configs/verifiers_v1.json"
    
    more_than_one_possible_combination_counter = 0

    game_setup_manager = GameSetupManager.from_json(game_setup_path)
    verifier_manager = VerifierManager()
    verifier_manager.load_verifiers_from_config(verifier_config_path)
    
    for setup_id in game_setup_manager.setups.keys():
        detected_active_criteria_ids, more_than_one_possible_combination_counter = auto_detect_actived_criteria(game_setup_manager.load_setup(setup_id), verifier_manager, more_than_one_possible_combination_counter)
        game_setup_manager.set_active_criteria_ids_by_setup_id(setup_id, detected_active_criteria_ids)
        print(f"SUCCESS: Setup {setup_id} detected active criteria ids: {detected_active_criteria_ids}")

    game_setup_manager.to_json(game_setup_path_new)
    print(f"More than one possible combination counter: {more_than_one_possible_combination_counter}")
if __name__ == "__main__":
    # single_game_setup_test(setup_id="20")
    multiple_game_setup_test()