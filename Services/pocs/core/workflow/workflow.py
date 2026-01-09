"""Workflow"""
import logging
from io import BytesIO
from PIL import Image

from langgraph.graph import StateGraph, END
from langchain_core.runnables.graph import MermaidDrawMethod

from pocs.agents.research_agent import ResearchAgent
from pocs.agents.evaluation_agent import EvaluationAgent
from pocs.agents.models.evaluation_state import EvaluationState
from pocs.agents.consolidation_agent import ConsolidationAgent
from pocs.agents.final_consolidation_agent import FinalConsolidationAgent


def run_with_part_name(name: str, run_fn: callable):
    """
    Decorator to add the node name to the state.
    """
    def wrapper(state):
        return run_fn(state, part_name=name)
    return wrapper


def start_node(state):
    """
    Start node.
    """
    logging.info("Start of the evaluation flow")
    return state


def create_workflow_sequential(workflow: StateGraph):
    """
    Create a sequential workflow.
    """
    workflow.set_entry_point("AGENT_A_PARTA")

    # Workflow for PART A
    workflow.add_edge("AGENT_A_PARTA", "AGENT_B_PARTA")
    workflow.add_edge("AGENT_B_PARTA", "CONSOLIDATOR_PARTA")

    # Workflow for PART B
    workflow.add_edge("CONSOLIDATOR_PARTA", "AGENT_A_PARTB")
    workflow.add_edge("AGENT_A_PARTB", "AGENT_B_PARTB")
    workflow.add_edge("AGENT_B_PARTB", "CONSOLIDATOR_PARTB")

    # Final consolidation
    workflow.add_edge("CONSOLIDATOR_PARTB", "FINAL_CONSOLIDATOR")
    workflow.add_edge("FINAL_CONSOLIDATOR", END)

    return workflow


def create_workflow_concurrent(workflow: StateGraph):
    """
    Create a concurrent workflow.
    """

    # Define entry point
    workflow.set_entry_point("START")

    workflow.add_edge("START", "RESEARCH_PARTA")
    workflow.add_edge("START", "RESEARCH_PARTB")

    # Workflow for PART A
    workflow.add_edge("RESEARCH_PARTA", "AGENT_A_PARTA")
    workflow.add_edge("RESEARCH_PARTA", "AGENT_B_PARTA")
    workflow.add_edge("AGENT_A_PARTA", "CONSOLIDATOR_PARTA")
    workflow.add_edge("AGENT_B_PARTA", "CONSOLIDATOR_PARTA")

    # Workflow for PART B
    workflow.add_edge("RESEARCH_PARTB", "AGENT_A_PARTB")
    workflow.add_edge("RESEARCH_PARTB", "AGENT_B_PARTB")
    workflow.add_edge("AGENT_A_PARTB", "CONSOLIDATOR_PARTB")
    workflow.add_edge("AGENT_B_PARTB", "CONSOLIDATOR_PARTB")

    # Workflow for FINAL
    workflow.add_edge("CONSOLIDATOR_PARTA", "FINAL_CONSOLIDATOR")
    workflow.add_edge("CONSOLIDATOR_PARTB", "FINAL_CONSOLIDATOR")
    workflow.add_edge("FINAL_CONSOLIDATOR", END)

    # Workflow for PART A
    # workflow.add_edge("START", "AGENT_A_PARTA")
    # workflow.add_edge("START", "AGENT_B_PARTA")
    # workflow.add_edge("AGENT_A_PARTA", "CONSOLIDATOR_PARTA")
    # workflow.add_edge("AGENT_B_PARTA", "CONSOLIDATOR_PARTA")

    # # Workflow for PART B
    # workflow.add_edge("START", "AGENT_A_PARTB")
    # workflow.add_edge("START", "AGENT_B_PARTB")
    # workflow.add_edge("AGENT_A_PARTB", "CONSOLIDATOR_PARTB")
    # workflow.add_edge("AGENT_B_PARTB", "CONSOLIDATOR_PARTB")

    # # Final consolidation
    # workflow.add_edge("CONSOLIDATOR_PARTA", "FINAL_CONSOLIDATOR")
    # workflow.add_edge("CONSOLIDATOR_PARTB", "FINAL_CONSOLIDATOR")
    # workflow.add_edge("FINAL_CONSOLIDATOR", END)

    return workflow


def create_workflow(evaluator_a: EvaluationAgent, evaluator_b: EvaluationAgent,
                    research_agent: ResearchAgent, consolidator: ConsolidationAgent, final_consolidator: FinalConsolidationAgent) -> StateGraph:
    """
    Creates a workflow for the evaluation process.
    """
    workflow = StateGraph(EvaluationState)

    # NODO START
    workflow.add_node("START", start_node)

    # Nodos para PARTE A
    workflow.add_node("RESEARCH_PARTA", run_with_part_name(
        "PARTA", research_agent.run))

    workflow.add_node("AGENT_A_PARTA", run_with_part_name(
        "PARTA", evaluator_a.run))
    workflow.add_node("AGENT_B_PARTA", run_with_part_name(
        "PARTA", evaluator_b.run))
    workflow.add_node("CONSOLIDATOR_PARTA", run_with_part_name(
        "PARTA", consolidator.run))

    # Nodos para PARTE B
    workflow.add_node("RESEARCH_PARTB", run_with_part_name(
        "PARTB", research_agent.run))
    workflow.add_node("AGENT_A_PARTB", run_with_part_name(
        "PARTB", evaluator_a.run))
    workflow.add_node("AGENT_B_PARTB", run_with_part_name(
        "PARTB", evaluator_b.run))
    workflow.add_node("CONSOLIDATOR_PARTB", run_with_part_name(
        "PARTB", consolidator.run))

    # Nodo para consolidación final
    workflow.add_node("FINAL_CONSOLIDATOR", run_with_part_name(
        "FINAL", final_consolidator.run))

    # SEQUENCIAL
    # create_workflow_sequential(workflow)
    # PARALLEL
    create_workflow_concurrent(workflow)

    # save_diagram(workflow)

    return workflow.compile()


def save_diagram(workflow: StateGraph):
    """
    Saves the diagram of the workflow.
    """
    # Save the workflow diagram
    try:
        # Compile the workflow and generate the diagram in PNG format
        compiled_graph = workflow.compile()
        png_bytes = compiled_graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API)

        # Verify that data was obtained
        if png_bytes:
            # Open the image from the bytes
            image = Image.open(BytesIO(png_bytes))

            # Save the image in a file
            image.save("./pocs/docs/workflow_diagram.jpg", format="JPEG")
            logging.info(
                "Workflow diagram saved successfully.")
        else:
            logging.error(
                "Failed to generate the workflow diagram: empty data.")
    except Exception as e:
        logging.error("Error saving the workflow diagram: %s", str(e))
