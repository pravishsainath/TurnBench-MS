import json
import re
import os

import pandas as pd


# Clean and process the DataFrame
def clean_option(value):
    if pd.isna(value):
        return ""
    # Extract middle three-digit number using regex
    try:
        split_value = value.split(" ")
        if len(split_value) < 3:
            raise Exception("Invalid value")
        match = split_value[1]
        
    except:
        match = value.replace(" ", "")[1:-3]
        print(f"Can't find match based on split, value is {value}, current match is {match}")
    if match == "" or match.isdigit() == False or int(match) > 48:
        print(f"Error: Invalid option {match}, value is {value}")
    return match

def clean_answer(value):
    return str(value).strip()

def extract_digits(value):
    match = re.search(r"(\d+)", str(value))
    return int(match.group(1)) if match else 0

def clean_question_id(qid):
    return qid.replace(" ", "")

def process_file(file_path, json_data):
    df = pd.read_csv(file_path)
    # Apply cleaning functions
    df["question_id"] = df["question_id"].apply(clean_question_id)
    df["A"] = df["A"].apply(clean_option)
    df["B"] = df["B"].apply(clean_option)
    df["C"] = df["C"].apply(clean_option)
    df["D"] = df["D"].apply(clean_option)
    if "E" in df.columns:
        df["E"] = df["E"].apply(clean_option)
    if "F" in df.columns:
        df["F"] = df["F"].apply(clean_option)
    df["answer"] = df["answer"].apply(clean_answer)

    # Convert to desired JSON format
    for _, row in df.iterrows():
        qid = row["question_id"]
        if qid in json_data:
            print(f"Error: Question ID {qid} already exists in JSON data")
            continue
        if "E" in df.columns and "F" in df.columns:
            verifiers_list = [int(row["A"]), int(row["B"]), int(row["C"]), int(row["D"]), int(row["E"]), int(row["F"])]
        elif "E" in df.columns:
            verifiers_list = [int(row["A"]), int(row["B"]), int(row["C"]), int(row["D"]), int(row["E"])]
        else:
            verifiers_list = [int(row["A"]), int(row["B"]), int(row["C"]), int(row["D"])]
        json_data[qid] = {
            "verifiers": verifiers_list,
            "active_criteria": [],
            "answer": row["answer"],
            "difficulty": row["difficulty"]
        }


def save_to_json(json_data, json_output_path):
    # Save to JSON file
    with open(json_output_path, "w") as f:
        json.dump(json_data, f, indent=4)

def main():
    file_folder_path = "/Users/grant/projects/uni_projects/game_benchmark/GameBench/data/game_setup_csv"
    json_data = {}
    for file_name in os.listdir(file_folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(file_folder_path, file_name)
            process_file(file_path, json_data)
    save_to_json(json_data, "/Users/grant/projects/uni_projects/game_benchmark/GameBench/data/configs/game_setups_new.json")

if __name__ == "__main__":
    main()
