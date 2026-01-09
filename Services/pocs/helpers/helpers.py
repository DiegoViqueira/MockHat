"""Helpers"""
import logging

from typing import Optional

from app.models.token_usage import TokensUsage
from pocs.agents.models.evaluation_state import EvaluationState
from pocs.helpers.report_generator import ReportGenerator


def load_from_file(file_path: str) -> Optional[str]:
    """
    Loads the content of a file.

    Args:
        file_path: The path to the file to load.

    Returns:
        str: The content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def print_tokens_usage(state: EvaluationState):
    """
    Calculates the total tokens used in the evaluation process.
    """
    final_tokens_usage = TokensUsage()

    evaluation_state = EvaluationState(**state)

    for evaluator_report in evaluation_state.evaluator_reports:
        final_tokens_usage += evaluator_report.tokens_usage

    for report in evaluation_state.consolidated_reports:
        final_tokens_usage += report.tokens_usage

    final_tokens_usage += evaluation_state.tokens_usage

    logging.info("Total tokens used %s",
                 final_tokens_usage.model_dump_json(indent=4))


def load_data(part: str):
    """
    Loads the data from the files for the specified part.
    """
    if part == "PARTA":
        return load_from_file("./pocs/data/criterios_valoracion_formateado.md"), load_from_file(f"./pocs/data/exam1/{part}/gpt4o_enunciado.txt"), load_from_file(f"./pocs/data/exam1/{part}/student/gpt_4o_student_{part.lower()}.txt")
    else:
        return load_from_file("./pocs/data/criterios_valoracion_formateado.md"), "", load_from_file(f"./pocs/data/exam1/{part}/student/gpt_4o_student_{part.lower()}.txt")


def generate_reports(final_state: EvaluationState):
    """
    Generates the report in markdown and pdf format.
    """
    # Generate reports
    output_md = "./pocs/data/exam1/multiple_agents_student_result.md"
    output_pdf = "./pocs/data/exam1/multiple_agents_student_result.pdf"
    output_json = "./pocs/data/exam1/multiple_agents_output.json"

    evaluation_state = EvaluationState(**final_state)

    ReportGenerator.save_markdown(
        evaluation_state.final_consolidated_report, output_md)
    ReportGenerator.generate_pdf(
        evaluation_state.final_consolidated_report, output_pdf)
    ReportGenerator.save_json(
        evaluation_state.model_dump_json(indent=4), output_json)
