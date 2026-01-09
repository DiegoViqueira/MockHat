"""Few Shot Factory"""
import logging
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, ChatPromptTemplate
from app.enums.level import Level
from app.enums.institution import Institution
from app.enums.writing_task import WritingTask
from app.databases.few_shot_writing_db import FewShotWritingDB


class FewShotWritingFactory:
    """
    This factory is used to create a few shot prompt for the writing task.
    """

    def __init__(self):
        self.few_shot_prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template(
                    "Assigned Task: {assigned_task}"),
                HumanMessagePromptTemplate.from_template(
                    "Answer to Evaluate: {task_answer}"),
                AIMessagePromptTemplate.from_template("{ai_answer}")
            ]
        )
        self.few_shot_db = FewShotWritingDB()

    def get_few_shot_prompt(self, institution: Institution, level: Level,  task: WritingTask) -> ChatPromptTemplate:
        """
        Get the few shot prompt for the writing task.
        """

        few_shot_samples = self.few_shot_db.get_few_shot_writing(
            institution, level, task)

        if few_shot_samples is None or len(few_shot_samples) == 0:
            logging.warning("!!!!!!!!!!!!!!!!!!!!!Few shot samples is empty")
            return None

        return self.few_shot_prompt.format_messages(**few_shot_samples)
