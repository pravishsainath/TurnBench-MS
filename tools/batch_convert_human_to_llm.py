#!/usr/bin/env python3
"""
Batch convert human experiment JSONs to LLM-like format.

Usage:
  python batch_convert_human_to_llm.py \
    --template /path/to/example_llm_result.json \
    --input_dir /path/to/human_experiment \
    --output_dir /path/to/converted_results

Arguments:
  --template     Path to a sample LLM result JSON file for extracting prompt keys.
  --input_dir    Root directory containing human experiment JSON files.
  --output_dir   Directory where converted JSON files will be saved.

Example:
  python batch_convert_human_to_llm.py \
    --template GameBench/data/results/deepseek-r1_deepseek_A5K9PT.json \
    --input_dir GameBench/data/human_experiment \
    --output_dir GameBench/converted_results
"""

import os
import json
import argparse


def load_template(template_path):
    """
    Load the 'game_prompts' structure from a sample LLM result file,
    but clear all prompt content to empty strings or empty dicts.

    :param template_path: Path to the sample LLM result JSON file.
    :return: A dict with the same keys as 'game_prompts', but empty values.
    """
    with open(template_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    prompts = data.get('game_prompts', {})
    empty_prompts = {}
    for key, value in prompts.items():
        if isinstance(value, str):
            empty_prompts[key] = ""
        elif isinstance(value, dict):
            empty_prompts[key] = {}
        else:
            empty_prompts[key] = None
    return empty_prompts


def convert_human_file(human_path, game_prompts, output_path):
    """
    Convert a single human experiment JSON file to the LLM-like format.

    :param human_path: Path to the human experiment JSON.
    :param game_prompts: A dict of empty game prompts structure.
    :param output_path: Path to write the converted JSON file.
    """
    with open(human_path, 'r', encoding='utf-8') as f:
        human = json.load(f)

    # Build the base structure
    converted = {
        'session_id': human.get('setup_id'),
        'model_name': 'human',
        'model_provider': 'manual',
        'setup': {
            'setup_id': human.get('setup_metadata', {}).get('setup_id'),
            'answer': human.get('setup_metadata', {}).get('answer'),
            'verifier_ids': human.get('setup_metadata', {}).get('verifier_ids', []),
            'active_criteria_ids': human.get('setup_metadata', {}).get('active_criteria_ids', []),
            'difficulty': human.get('setup_metadata', {}).get('difficulty'),
            'nightmare_verifier_ids': [],
            'nightmare_active_criteria_ids': []
        },
        'max_rounds': len(human.get('rounds_data', [])),
        'game_prompts': game_prompts
    }

    # Compute game state
    rounds = human.get('rounds_data', [])
    total_questions = sum(len(r.get('question', [])) for r in rounds)
    last_round = rounds[-1] if rounds else {}
    ded_src = last_round.get('deduce', {})

    converted['game_state'] = {
        'total_rounds': len(rounds),
        'verifier_uses_total': total_questions,
        'game_over': human.get('game_over_reason') == 'submitted_answer',
        'game_over_reason': human.get('game_over_reason'),
        'submitted_code': ded_src.get('submitted_code'),
        'success': ded_src.get('guess_correct'),
        'num_of_verifier_passed': ded_src.get('num_of_verifier_passed'),
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'total_prompt_cache_hit_tokens': 0,
        'total_reasoning_tokens': 0,
        'total_response_with_formatting_error': 0,
        'total_response_with_not_valid_error': 0,
        'longest_context_length': 0,
        'with_reasoning': True,
        'with_hint': True,
        'mode': human.get('setup_metadata', {}).get('mode'),
        'total_time': human.get('total_elapsed_time_seconds'),
        'all_guesses': [r.get('proposal', {}).get('guess_code') for r in rounds],
        'all_verifier_choices': [
            [[q.get('verifier_choice'), q.get('verifier_result')] for q in r.get('question', [])]
            for r in rounds
        ]
    }

    # Build round_history with empty model_reasoning
    processed_rounds = []
    for r in rounds:
        prop_src = r.get('proposal', {})
        proposal = {
            'guess_code': prop_src.get('guess_code'),
            'reasoning': prop_src.get('reasoning'),
            'model_reasoning': ''
        }
        questions = []
        for q in r.get('question', []):
            questions.append({
                'verifier_choice': q.get('verifier_choice'),
                'verifier_result': q.get('verifier_result'),
                'reasoning': q.get('reasoning'),
                'model_reasoning': ''
            })
        ded_src = r.get('deduce', {})
        deduce = {
            'submitted': ded_src.get('submitted', False),
            'submitted_code': ded_src.get('submitted_code'),
            'guess_correct': ded_src.get('guess_correct'),
            'reasoning': ded_src.get('reasoning'),
            'model_reasoning': ''
        }
        processed_rounds.append({
            'proposal': proposal,
            'question': questions,
            'deduce': deduce
        })

    converted['round_history'] = processed_rounds
    converted['messages'] = []

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(converted, out_f, ensure_ascii=False, indent=2)
    print(f"Converted: {human_path} -> {output_path}")


def batch_convert(template_path, input_dir, output_root):
    """
    Convert all human experiment JSON files under input_dir to LLM-like format.

    :param template_path: Path to a sample LLM result JSON file for extracting prompts.
    :param input_dir: Root directory containing human experiment JSONs.
    :param output_root: Directory where converted JSONs will be saved.
    """
    game_prompts = load_template(template_path)
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if not fname.endswith('.json'):
                continue
            human_path = os.path.join(root, fname)
            rel_dir = os.path.relpath(root, input_dir)
            output_dir = os.path.join(output_root, rel_dir)
            output_path = os.path.join(output_dir, fname)
            convert_human_file(human_path, game_prompts, output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Batch convert human experiment JSONs to LLM-like format.')
    parser.add_argument(
        '--template',
        required=True,
        help='Path to a sample LLM result JSON file for extracting prompts.'
    )
    parser.add_argument(
        '--input_dir',
        required=True,
        help='Root folder of human experiment JSON files.'
    )
    parser.add_argument(
        '--output_dir',
        required=True,
        help='Directory to save the converted JSON files.'
    )
    args = parser.parse_args()

    batch_convert(args.template, args.input_dir, args.output_dir)


if __name__ == '__main__':
    main()
