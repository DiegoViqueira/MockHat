"""This file contains the prompts for the agents."""

import os


def load_prompt(prompt_name: str):
    """Load the evaluator prompt from the file."""
    with open(os.path.join(os.path.dirname(__file__), f"{prompt_name}.MD"), "r", encoding="utf-8") as f:
        return f.read()


EVALUATOR_PROMPT = load_prompt("EVALUATOR")
CONSOLIDATOR_PROMPT = load_prompt("CONSOLIDATOR")
FINAL_CONSOLIDATOR_PROMPT = load_prompt("FINAL_CONSOLIDATOR")
RESEARCH_PROMPT = load_prompt("RESEARCH")
