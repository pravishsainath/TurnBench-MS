import random

from dotenv import load_dotenv

from core.experiment_manager import ExperimentManager
from configs.config import get_config
from utils.tools import load_json_file

load_dotenv()

def random_guess() -> str:
    """return a random 3-digit number"""
    digit1 = random.randint(1, 5)
    digit2 = random.randint(1, 5)
    digit3 = random.randint(1, 5)
    return f"{digit1}{digit2}{digit3}"

def single_game_random_guess(setup: dict) -> int:
    random_guess_results = []
    for setup_id, setup in setup.items():
        guess = random_guess()
        answer = setup["answer"]
        if guess == answer:
            random_guess_results.append(1)
        else:
            random_guess_results.append(0)

    return sum(random_guess_results) / len(random_guess_results)

def main():
    setup_path = "data/configs/game_setups_270.json"
    all_setups = load_json_file(setup_path)

    random_guess_results = []
    for _ in range(1000):
        random_guess_results.append(single_game_random_guess(all_setups))

    print(sum(random_guess_results) / len(random_guess_results))


    

    

if __name__ == "__main__":
    main()