from langsmith import Client


def load_prompt(prompt_name: str):
    """Load the evaluator prompt from the file."""
    print("Loading prompt: %s", prompt_name)
    langsmith_client = Client()
    prompt = langsmith_client.pull_prompt(prompt_name)
    return prompt


WRITING_CORRECTION_PROMPT = load_prompt("writing_correction_chain")
GRAMMAR_CORRECTION_PROMPT = load_prompt("grammar_correction_chain")
IMAGE_TRANSCRIBER_PROMPT = load_prompt("image_transcriber_chain")
CLASS_ANALYSIS_PROMPT = load_prompt("class_analysis_chain")
