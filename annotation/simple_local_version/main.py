import json, os, datetime
from datetime import datetime, timezone, timedelta

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from utils.tools import load_yaml_config, save_json_file, load_json_file
from verifier.verifier_manager import VerifierManager
from annotation.simple_local_version.models import (
    GameData, 
    GameSession, 
    SetupMetadata, 
    RoundResultModel, 
    ProposalResultModel, 
    QuestionResultModel,
    DeduceResultModel
)
from annotation.simple_local_version.step_explanation import (
    proposal_explanation,
    question_explanation,
    dudecode_explanation
)
from typing import Optional

app = FastAPI()

config = load_yaml_config("annotation/simple_local_version/config.yaml")
root_result_dir = config["result_dir"]
os.makedirs(root_result_dir, exist_ok=True)

MAX_ROUNDS = config["max_rounds"]

game_setups_dir = config["game_setups_dir"]
game_setups = load_json_file(game_setups_dir)

verifier_manager = VerifierManager.from_json(config["verifier_manager_dir"])

app.mount("/static", StaticFiles(directory="annotation/simple_local_version/static"), name="static")
templates = Jinja2Templates(directory="annotation/simple_local_version/templates")

game_data = None
active_game_session = None 

def format_elapsed_time(start_time: Optional[datetime]) -> str:
    """Calculates elapsed time and formats it as MM:SS."""
    if start_time is None:
        return "N/A"
    
    # Ensure start_time is offset-aware or convert now() to offset-naive
    # Easiest is to make sure both are naive or both are aware
    # If start_time might be naive (e.g. from older saves):
    if start_time.tzinfo is None:
        now_naive = datetime.now()
        elapsed = now_naive - start_time
    else:
        # If start_time is aware (e.g. using timezone.utc):
        now_aware = datetime.now(start_time.tzinfo) # Use same timezone
        elapsed = now_aware - start_time

    total_seconds = int(elapsed.total_seconds())
    if total_seconds < 0: total_seconds = 0 # Prevent negative time display
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def load_or_create_game_data(name: str, root_dir: str) -> None:
    global game_data
    file_path = os.path.join(root_dir, f"{name.replace(' ', '-')}.json")
    if os.path.exists(file_path):
        data = load_json_file(file_path)
        game_data = GameData(**data)
    else:
        game_data = GameData()
        game_data.metadata.name = name

def get_game_data() -> GameData:
    if game_data is None:
        raise RuntimeError("GameData is not initialized. Call /start first.")
    return game_data

def save_game_data() -> None:
    current_game_data = get_game_data()
    folder_name = os.path.join(root_result_dir, current_game_data.metadata.name.replace(' ', '-'))
    os.makedirs(folder_name, exist_ok=True)
    file_name = os.path.join(folder_name, f"{current_game_data.metadata.name.replace(' ', '-')}.json")
    print(f"Saving game data to: {file_name}")
    save_json_file(current_game_data.model_dump(), file_name)

def get_active_game_session() -> GameSession:
    global active_game_session
    if active_game_session is None:
        raise RuntimeError("Active game session is not initialized. Call /select-game first.")
    return active_game_session

def save_active_game_session() -> None:
    try:
        game_session = get_active_game_session()
        user_name = get_game_data().metadata.name
        session_game_id = game_session.setup_id
        folder_name = os.path.join(root_result_dir, user_name.replace(" ", "-"), game_session.setup_metadata.mode)
        os.makedirs(folder_name, exist_ok=True)
        file_name = os.path.join(folder_name, f"{session_game_id}.json")
        print(f"Saving active session to: {file_name}")
        save_json_file(game_session.model_dump(mode='json', exclude_none=True), file_name)
    except (RuntimeError, TypeError) as e:
        print(f"Error saving session: {e}")

def load_active_game_session(user_name: str, game_id: str) -> None:
    global active_game_session
    mode = game_setups[game_id].get("mode", "classic")
    folder_name = os.path.join(root_result_dir, user_name.replace(" ", "-"), mode)
    file_path = os.path.join(folder_name, f"{game_id}.json")
    if os.path.exists(file_path):
        try: # Added try-except for robust loading
            loaded_data = load_json_file(file_path)
            active_game_session = GameSession(**loaded_data)
            # Check if loaded session has start_time, if not, set it
            if active_game_session.start_time is None:
                print(f"Setting start time for previously saved session {game_id}")
                active_game_session.start_time = datetime.now()
                # Optionally save immediately after adding start_time
                # save_active_game_session() # Be careful about potential recursion if called within load
            print(f"Loaded active session from: {file_path}")
        except Exception as e: # Catch potential Pydantic validation errors etc.
             print(f"Error loading/validating session file {file_path}, creating new. Error: {e}")
             active_game_session = None # Ensure it's reset if load fails
    
    # If load failed, session is None, or ID mismatch
    if active_game_session is None or active_game_session.setup_id != game_id: 
        if active_game_session is not None: 
             print(f"Warning: Loaded session ID '{active_game_session.setup_id}' doesn't match requested '{game_id}'. Creating new.")
        
        verifier_ids_for_description = game_setups[game_id].get("verifier_ids", [])
        active_criteria_ids_for_description = game_setups[game_id].get("active_criteria_ids", [])
        verifier_ids = game_setups[game_id].get("verifier_ids" if mode == "classic" else "nightmare_verifier_ids", [])
        active_criteria_ids = game_setups[game_id].get("active_criteria_ids" if mode == "classic" else "nightmare_active_criteria_ids", [])
        active_game_session = GameSession(
            setup_id=game_id,
            start_time=datetime.now(), # Set start time for new session
            setup_metadata=SetupMetadata(
                setup_id=game_id,
                verifier_ids=verifier_ids,
                active_criteria_ids=active_criteria_ids,
                answer=game_setups[game_id].get("answer", ""),
                difficulty=game_setups[game_id].get("difficulty", ""),
                mode=mode,
                verifier_details=verifier_manager.get_verifier_descriptions(verifier_ids_for_description)
            )
        )
        print(f"Created new session for game {game_id}, mode: {mode}")
        active_game_session.rounds_data.append(RoundResultModel())


def list_all_game_setups():
    setups = []
    current_game_data = get_game_data()
    finished_setups = current_game_data.metadata.finished_setups

    for game_setup_id, game_setup_metadata in game_setups.items():
        verifier_ids = game_setup_metadata.get("verifier_ids", [])
        difficulty = game_setup_metadata.get("difficulty", "N/A")
        mode = game_setup_metadata.get("mode", "classic")
        setups.append({
            "finished": game_setup_id in finished_setups,
            "game_setup_id": game_setup_id, 
            "number_of_verifiers": len(verifier_ids),
            "difficulty": difficulty,
            "mode": mode
        })
    
    difficulty_order = {"easy": 0, "medium": 1, "hard": 2}
    
    setups.sort(key=lambda x: (
        x["finished"], 
        difficulty_order.get(x["difficulty"].lower(), 99),
        x["number_of_verifiers"]
    ))
    
    return setups

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start")
def start_game(request: Request, name: str = Form(...)):
    load_or_create_game_data(name, root_result_dir)
    save_game_data()
    return RedirectResponse(url="/game-list", status_code=303)

@app.get("/game-list")
def get_game_list(request: Request):
    try:
        return templates.TemplateResponse("game_list.html", {
            "request": request,
            "games": list_all_game_setups()
        })
    except Exception as e:
        return RedirectResponse(url="/", status_code=303)
    
@app.post("/select-game")
def select_game(game_id: str = Form(...)):
    if game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
    try:
        user_name = get_game_data().metadata.name
        load_active_game_session(user_name, game_id)
        save_active_game_session() 
    except RuntimeError:
        print("Error: User data not loaded. Cannot initialize session.")
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        print(f"Error during session load/save in /select-game: {e}")
        return RedirectResponse(url="/game-list", status_code=303)

    proposal_url = f"/game/{game_id}/proposal"
    return RedirectResponse(url=proposal_url, status_code=303)

@app.get("/game/{game_id}/proposal")
def get_proposal_page(request: Request, game_id: str):
    if game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
    try:
        session = get_active_game_session()
        if session.setup_id != game_id:
            print(f"Warning: URL game_id '{game_id}' does not match active session setup_id '{session.setup_id}'.")
            return RedirectResponse(url="/game-list", status_code=303)

    except RuntimeError:
        return RedirectResponse(url="/game-list", status_code=303)

    verifier_description_string = session.setup_metadata.verifier_details
    if not verifier_description_string:
        verifier_description_string = "No verifier details provided."

    elapsed_time_str = format_elapsed_time(session.start_time)

    context = {
        "request": request,
        "game_id": game_id,
        "difficulty": session.setup_metadata.difficulty,
        "mode": session.setup_metadata.mode,
        "round_number": session.current_round_number,
        "step_title": "Compose the Proposal",
        "round_description": proposal_explanation,
        "verifier_description": verifier_description_string,
        "elapsed_time": elapsed_time_str
    }
    return templates.TemplateResponse("proposal.html", context)

@app.post("/game/{game_id}/submit-proposal")
async def submit_proposal(request: Request, game_id: str, 
                         thinking_process: str = Form(...), 
                         guess_code: str = Form(...)):
    if game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
    try:
        session = get_active_game_session()
        if session.setup_id != game_id:
             return RedirectResponse(url="/game-list", status_code=303)
        
        round_index = session.current_round_number - 1
        if round_index < 0 or round_index > len(session.rounds_data):
            raise IndexError("Round data not initialized correctly.")
        if len(session.rounds_data) <= round_index:
            session.rounds_data.append(RoundResultModel())
            
        session.rounds_data[round_index].proposal = ProposalResultModel(
            guess_code=guess_code,
            reasoning=thinking_process
        )
        save_active_game_session()

    except (RuntimeError, TypeError, IndexError) as e:
        print(f"Error submitting proposal: {e}")
        return RedirectResponse(url=f"/game/{game_id}/proposal", status_code=303) 

    question_url = f"/game/{game_id}/question"
    return RedirectResponse(url=question_url, status_code=303)

@app.get("/game/{game_id}/question")
def get_question_page(request: Request, game_id: str):
    if game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
    
    last_action = None # Initialize default
    try:
        session = get_active_game_session()
        if session.setup_id != game_id:
            return RedirectResponse(url="/game-list", status_code=303)

        # Read and immediately reset last_action
        last_action = session.last_action
        session.last_action = None 
        # Save the reset state (important!)
        save_active_game_session() 

        round_index = session.current_round_number - 1
        if round_index < 0 or round_index > len(session.rounds_data):
             raise IndexError("Round data not initialized correctly.")
         
        if len(session.rounds_data) <= round_index:
            session.rounds_data.append(RoundResultModel())

        current_round_data = session.rounds_data[round_index]
        questions_asked = current_round_data.question
        num_questions_asked = len(questions_asked)
        max_questions = 3
        
        q_num_ordinal = {1: "1st", 2: "2nd", 3: "3rd"}
        # Calculate based on the *potential* next question index if we just clicked "next"
        next_question_display_num = num_questions_asked + 1 if last_action == "next" else num_questions_asked
        if next_question_display_num == 0: next_question_display_num = 1 # Ensure it starts at 1st
            
        verifier_label = f"Choose {q_num_ordinal.get(next_question_display_num, f'{next_question_display_num}th')} Verifier"
        if next_question_display_num > max_questions:
            verifier_label = "Max verifiers reached"

        last_question_result = None
        last_thinking_process = ""
        
        # Decide what to display based on the action that led here
        if last_action == "verify" and questions_asked:
            # Just verified, show the result and reasoning of the last question
            last_question_result = questions_asked[-1].verifier_result
            last_thinking_process = questions_asked[-1].reasoning or ""
        # Else (last_action was "next" or None/first load): result stays None, thinking stays ""

    except (RuntimeError, TypeError, IndexError) as e:
        print(f"Error getting session/data for question page: {e}")
        return RedirectResponse(url="/game-list", status_code=303)

    verifier_description_string = session.setup_metadata.verifier_details # Assuming session is available from try block
    if not verifier_description_string:
        verifier_description_string = "No verifier details provided."
        
    elapsed_time_str = format_elapsed_time(session.start_time)

    context = {
        "request": request,
        "game_id": game_id,
        "difficulty": session.setup_metadata.difficulty,
        "mode": session.setup_metadata.mode,
        "round_number": session.current_round_number,
        "step_title": "Question Verifiers",
        "round_description": question_explanation,
        "verifier_description": verifier_description_string,
        "verifier_label": verifier_label,
        # Determine if user can ask based on *actual* number asked vs max
        "can_ask_more": num_questions_asked < max_questions, 
        "last_verifier_result": last_question_result, # Will be None after "next"
        "existing_thinking_process": last_thinking_process, # Will be "" after "next"
        "elapsed_time": elapsed_time_str
    }
    return templates.TemplateResponse("question.html", context)

@app.post("/game/{game_id}/submit-question")
async def submit_question(request: Request, game_id: str, 
                           thinking_process: str = Form(...), 
                           verifier_number: str = Form(...),
                           action: str = Form(...)):
    
    if action != "verify" or game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
        
    try:
        session = get_active_game_session()
        if session.setup_id != game_id:
             return RedirectResponse(url="/game-list", status_code=303)
             
        round_index = session.current_round_number - 1
        if round_index < 0 or round_index > len(session.rounds_data):
             raise IndexError("Round data not initialized correctly.")
        
        if len(session.rounds_data) <= round_index:
            session.rounds_data.append(RoundResultModel())

        chosen_verifier_index = -1
        try:
            if not verifier_number.isdigit() or len(verifier_number) != 1:
                 raise ValueError("Verifier choice must be a single digit index (0-based potentially).")
            chosen_verifier_index = int(verifier_number)
            
            # Validate index range
            if not (0 <= chosen_verifier_index < len(session.setup_metadata.verifier_ids)):
                raise ValueError(f"Verifier index {chosen_verifier_index} out of range.")
                
        except ValueError as e:
            print(f"Invalid verifier number submitted: {verifier_number}. Error: {e}")
            return RedirectResponse(url=f"/game/{game_id}/question", status_code=303)
        
        proposal_code = session.rounds_data[round_index].proposal.guess_code
        print(f"DEBUG: Simulating check: Verifier {chosen_verifier_index} against code '{proposal_code}'")
        vid = session.setup_metadata.verifier_ids[chosen_verifier_index]
        active_criterian = session.setup_metadata.active_criteria_ids[chosen_verifier_index]
        # print("DEBUG: vid: ", vid, "active_criterian: ", active_criterian)
        # debug_verifier_dict = verifier_manager.get_verifier_dict_by_id(vid)
        # print("DEBUG: debug_verifier_dict: ", debug_verifier_dict)
        # print("DEBUG: active_criterian: ", debug_verifier_dict["criteria"][active_criterian])
        verify_result = verifier_manager.verify(vid, proposal_code, active_criterian)
        verification_result_str = "PASS" if verify_result else "FAIL" # Changed from TRUE/FAIL
        print(f"DEBUG: Result: {verification_result_str}")
        
        current_round_data = session.rounds_data[round_index]
        num_questions_asked = len(current_round_data.question)
        max_questions = 3

        if num_questions_asked < max_questions:
            question_data = QuestionResultModel(
                 verifier_choice=str(chosen_verifier_index),
                 verifier_result=verification_result_str, 
                 reasoning=thinking_process
            )
            
            current_question_index = num_questions_asked
            
            if current_question_index < len(current_round_data.question):
                 print(f"Updating existing question at index {current_question_index}")
                 current_round_data.question[current_question_index] = question_data
            else:
                 current_round_data.question.append(question_data)

            session.last_action = "verify"
            save_active_game_session()
        else:
            print("Warning: Max questions already asked for this round.")

    except (RuntimeError, TypeError, IndexError, ValueError) as e:
        print(f"Error submitting question: {e}")
        return RedirectResponse(url=f"/game/{game_id}/question", status_code=303)

    return RedirectResponse(url=f"/game/{game_id}/question", status_code=303)

@app.post("/game/{game_id}/next-question")
async def next_question(request: Request, game_id: str, action: str = Form(...)):
    if action != "next_question" or game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
        
    try:
        session = get_active_game_session()
        if session.setup_id != game_id:
             return RedirectResponse(url="/game-list", status_code=303)
             
        round_index = session.current_round_number - 1
        if round_index < 0 or round_index > len(session.rounds_data):
             raise IndexError("Round data not initialized correctly.")

        current_round_data = session.rounds_data[round_index]
        num_questions_asked = len(current_round_data.question)
        max_questions = 3

        if num_questions_asked < max_questions:
             # Set the last action before saving
             session.last_action = "next"
             save_active_game_session()
        else:
            print("Info: Cannot move to next question, max limit reached.")

    except (RuntimeError, TypeError, IndexError) as e:
        print(f"Error during next question: {e}")
        return RedirectResponse(url=f"/game/{game_id}/question", status_code=303)

    return RedirectResponse(url=f"/game/{game_id}/question", status_code=303)

@app.get("/game/{game_id}/deduce")
def get_deduce_page(request: Request, game_id: str):
    if game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
    try:
        session = get_active_game_session()
        if session.setup_id != game_id:
            return RedirectResponse(url="/game-list", status_code=303)

        round_index = session.current_round_number - 1
        existing_thinking_process = ""
        # Load thinking process if it exists for deduce step in current round
        if 0 <= round_index < len(session.rounds_data):
            existing_thinking_process = session.rounds_data[round_index].deduce.reasoning or ""
            
    except (RuntimeError, TypeError, IndexError) as e:
        print(f"Error getting session/data for deduce page: {e}")
        return RedirectResponse(url="/game-list", status_code=303)

    verifier_description_string = session.setup_metadata.verifier_details
    if not verifier_description_string:
        verifier_description_string = "No verifier details provided."
        
    elapsed_time_str = format_elapsed_time(session.start_time)

    context = {
        "request": request,
        "game_id": game_id,
        "difficulty": session.setup_metadata.difficulty,
        "mode": session.setup_metadata.mode,
        "round_number": session.current_round_number,
        "step_title": "Deduce Answer", # Updated title
        "round_description": dudecode_explanation, # Use imported explanation
        "verifier_description": verifier_description_string,
        "existing_thinking_process": existing_thinking_process, # Pre-fill if exists
        "elapsed_time": elapsed_time_str
    }
    return templates.TemplateResponse("deduce.html", context)

@app.post("/game/{game_id}/submit-deduction")
async def submit_deduction(request: Request, game_id: str,
                           thinking_process: str = Form(...),
                           submitted_code: str = Form(...), 
                           round_number: int = Form(...)):
    
    if game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
        
    try:
        session = get_active_game_session()
        user_data = get_game_data() 
        if session.setup_id != game_id or session.current_round_number != round_number:
             print(f"Warning: Session state mismatch (game_id or round_number).")
             return RedirectResponse(url="/game-list", status_code=303) # Redirect to list if state seems wrong

        round_index = session.current_round_number - 1
        if round_index < 0:
             raise IndexError("Invalid round index calculated.")
             
        while len(session.rounds_data) <= round_index:
             session.rounds_data.append(RoundResultModel())

        # --- Calculate elapsed time (needed in both branches) --- 
        final_elapsed_seconds = 0
        if session.start_time:
             final_elapsed_seconds = int((datetime.now(session.start_time.tzinfo if session.start_time.tzinfo else None) - session.start_time).total_seconds())
             if final_elapsed_seconds < 0: final_elapsed_seconds = 0
        session.total_elapsed_time_seconds = final_elapsed_seconds # Store time in session

        # --- Logic based on submitted_code --- 
        if not submitted_code:
            # --- Trying to Start Next Round --- 
            print(f"No code submitted for round {session.current_round_number}. Checking round limit.")
            # Save current round's deduce reasoning (even if game ends here)
            session.rounds_data[round_index].deduce = DeduceResultModel(
                submitted=False, 
                reasoning=thinking_process 
            )
            
            next_round_number = session.current_round_number + 1
            if next_round_number > MAX_ROUNDS:
                # --- Game Over: Max Rounds Reached --- 
                print(f"Max rounds ({MAX_ROUNDS}) reached. Ending game.")
                session.game_over_reason = "max_rounds_reached"
                session.last_action = "deduce_max_rounds" # Specific action
                # Final deduce result indicates failure due to max rounds
                session.rounds_data[round_index].deduce.guess_correct = False 
                session.rounds_data[round_index].deduce.submitted = False # Indicate didn't submit code this round
                
                # Mark game finished in user's overall progress
                if game_id not in user_data.metadata.finished_setups:
                    user_data.metadata.finished_setups.append(game_id)
                    save_game_data()
                
                save_active_game_session()
                return RedirectResponse(url=f"/game/{game_id}/game-over", status_code=303)
            else:
                # --- Proceed to Next Round --- 
                session.current_round_number = next_round_number
                session.last_action = None # Reset last action for new round
                save_active_game_session()
                return RedirectResponse(url=f"/game/{game_id}/proposal", status_code=303)
        else:
            # --- Submitted Final Answer --- 
            print(f"Final code submitted for round {session.current_round_number}: {submitted_code}")
            correct_answer = session.setup_metadata.answer
            is_correct = (submitted_code == correct_answer)
            print(f"Correct Answer: {correct_answer}, Guess Correct: {is_correct}")

            num_passed = 0
            # Note: This verifies against the *submitted_code*, not proposal_code
            for i, vid in enumerate(session.setup_metadata.verifier_ids):
                 if verifier_manager.verify(vid, submitted_code, session.setup_metadata.active_criteria_ids[i]):
                     num_passed += 1
                
            session.rounds_data[round_index].deduce = DeduceResultModel(
                submitted=True,
                submitted_code=submitted_code,
                guess_correct=is_correct,
                reasoning=thinking_process,
                num_of_verifier_passed=num_passed
                # total_elapsed_time_seconds removed from here
            )
            session.game_over_reason = "submitted_answer" # Set reason
            session.last_action = "deduce_submitted"
            
            if game_id not in user_data.metadata.finished_setups:
                 user_data.metadata.finished_setups.append(game_id)
                 save_game_data()
                 
            save_active_game_session()
            return RedirectResponse(url=f"/game/{game_id}/game-over", status_code=303)

    except (RuntimeError, TypeError, IndexError, ValueError) as e:
        print(f"Error submitting deduction: {e}")
        # Attempt to clear potentially inconsistent last_action
        try:
            session = get_active_game_session()
            session.last_action = None
            save_active_game_session()
        except: pass # Ignore errors during cleanup
        return RedirectResponse(url=f"/game/{game_id}/deduce", status_code=303)

@app.get("/game/{game_id}/game-over")
def get_game_over_page(request: Request, game_id: str):
    # Declare global at the beginning of the function scope
    global active_game_session 
    
    if game_id not in game_setups:
        return RedirectResponse(url="/game-list", status_code=303)
    
    session_data_for_template = None
    try:
        # No need for global declaration here anymore
        session = get_active_game_session() # This function handles the global access internally if needed
        # Check if game actually ended based on last action/reason
        if session.setup_id != game_id or session.game_over_reason is None:
            print("Warning: Invalid access to game-over page (game not ended or session mismatch).")
            return RedirectResponse(url="/game-list", status_code=303)
            
        round_index = session.current_round_number - 1
        if round_index < 0 or round_index >= len(session.rounds_data):
            raise IndexError("Cannot find final round data.")
        
        final_deduce_result = session.rounds_data[round_index].deduce
        
        # Determine correctness based on reason
        is_correct_final = False
        if session.game_over_reason == "submitted_answer":
            is_correct_final = final_deduce_result.guess_correct
        
        # Format total time
        total_time_str = "N/A"
        if session.total_elapsed_time_seconds is not None:
             minutes = session.total_elapsed_time_seconds // 60
             seconds = session.total_elapsed_time_seconds % 60
             total_time_str = f"{minutes:02d}:{seconds:02d}"
             
        # Prepare context data BEFORE resetting session
        session_data_for_template = {
            "game_id": game_id,
            "guess_correct": is_correct_final, # Use derived correctness
            "submitted_code": final_deduce_result.submitted_code,
            "answer": session.setup_metadata.answer,
            "game_over_reason": session.game_over_reason,
            "total_time_str": total_time_str,
        }
        
        # Reset the global session variable (using the global declared at the top)
        active_game_session = None 
        print(f"Active game session for {game_id} reset after displaying game over.")
        
    except (RuntimeError, TypeError, IndexError) as e:
        print(f"Error getting session/data for game over page: {e}")
        # If session exists but error occurred, try to clear it before redirecting
        try:
            # No need for global here either, already declared for the function
            active_game_session = None
        except: pass 
        return RedirectResponse(url="/game-list", status_code=303)
    except Exception as e: # Catch any other unexpected error
        print(f"Unexpected error on game over page: {e}")
        # Use the global declared at the top
        active_game_session = None # Ensure session clear on any error
        return RedirectResponse(url="/game-list", status_code=303)
        
    if session_data_for_template is None:
         print("Error: Session data for template was not prepared.")
         return RedirectResponse(url="/game-list", status_code=303)

    context = {"request": request, **session_data_for_template}
    return templates.TemplateResponse("game_over.html", context)

