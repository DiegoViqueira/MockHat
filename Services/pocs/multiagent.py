"""Multiagent"""
import asyncio
import logging


from app.enums.deployment import Deployment
from app.enums.provider import Provider
from app.factories.language_model_factory import LanguageModelFactory
from pocs.agents.research_agent import ResearchAgent
from pocs.agents.models.evaluation_criteria import EvaluationCriteria
from pocs.agents.models.evaluation_state import EvaluationState
from pocs.core.workflow.workflow import create_workflow
from pocs.helpers.helpers import generate_reports, load_data,  print_tokens_usage
from pocs.agents.consolidation_agent import ConsolidationAgent
from pocs.agents.evaluation_agent import EvaluationAgent
from pocs.agents.final_consolidation_agent import FinalConsolidationAgent
from pocs.agents.models.student_response import StudentResponse


# Logging Configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


# Language Models
llama_model = LanguageModelFactory.create_model(
    Provider.GROQ, Deployment.LLAMA4).model
gpt_model = LanguageModelFactory.create_model(
    Provider.AZURE, Deployment.GPT_4O).model


async def main():
    """Main function that executes the evaluation process."""
    try:
        # Initialize agents
        evaluator_a = EvaluationAgent(llama_model, "A")
        evaluator_b = EvaluationAgent(gpt_model, "B")
        research_agent = ResearchAgent(llama_model, "Research")
        consolidator = ConsolidationAgent(gpt_model)
        final_consolidator = FinalConsolidationAgent(gpt_model)

        # Create workflow
        workflow = create_workflow(
            evaluator_a, evaluator_b, research_agent, consolidator, final_consolidator)

        # Load and process PART A
        criterio_de_valoracion, enunciado_parta, respuesta_parta = load_data(
            "PARTA")
        if not all([criterio_de_valoracion, enunciado_parta, respuesta_parta]):
            raise ValueError("Error al cargar los archivos de PARTE A")

        # Load and process PART B
        _, _, respuesta_partb = load_data("PARTB")
        if not all([respuesta_partb]):
            raise ValueError("Error al cargar los archivos de PARTE B")

        # Create initial state with both parts

        initial_state = EvaluationState(
            evaluation_criteria=[
                EvaluationCriteria(
                    section_name="PARTA",
                    enunciation=enunciado_parta,
                    criteria=criterio_de_valoracion
                ),
                EvaluationCriteria(
                    section_name="PARTB",
                    criteria=criterio_de_valoracion
                )
            ],
            student_responses=[
                StudentResponse(
                    section_name="PARTA",
                    response=respuesta_parta
                ),
                StudentResponse(
                    section_name="PARTB",
                    response=respuesta_partb
                )
            ],
        )

        # Execute evaluation
        final_state = workflow.invoke(initial_state)

        print_tokens_usage(final_state)

        # Generate reports
        generate_reports(final_state)

        logging.info("Process completed successfully")

    except Exception as e:
        logging.error("Error in the main process: %s", str(e)[:100])
        raise

if __name__ == "__main__":
    asyncio.run(main())
