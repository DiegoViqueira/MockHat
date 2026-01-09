"""Writing Transcribe Prompt Factory"""
from app.enums.writing_task import WritingTask


class WritingTranscribePromptFactory:
    """
    This factory is used to create a prompt for the writing translation task.
    """

    def __init__(self):
        self.prompts_mapping = {
            WritingTask.EMAIL: """
            I'm going to provide you with an image of a writing task, which is an email. 
            The input consists of a standard rubric, an email with its structure (to,from,subject and body), and a set of annotations or note that are linked by lines to the appropriate parts of the input email text. 
            Your task is to extract each of these elements: 
             - The standard rubric
             - The email (to, from, subject, body)
             - The notes
            If any of these parts (rubric, to, from, subject, body, or notes) are missing in the input, do not include them in the output.
            Do not take into consideration or transcribe strikedthrough words.
             Here is an example of the expected format: 
                Rubric:  [rubric content if present]
                To:  [to content if present]
                From: [from content if present]
                Subject: [subject content if present]
                Boby: [body content if present]
                Notes: [notes content if any note is present]
                - Note 1:
                  Note: [note]
                  Email Part: [email part of the note]
                """,
            WritingTask.STORY: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words. ",
            WritingTask.ARTICLE: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
            WritingTask.REVIEW: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words. ",
            WritingTask.REPORT: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words. ",
            WritingTask.ESSAY: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words. ",
            WritingTask.PROPOSAL: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
            WritingTask.FOR_AND_AGAINST_ESSAY: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
            WritingTask.FORMAL_APPLICATION_EMAIL: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
            WritingTask.FORMAL_COMPLAINT_EMAIL: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
            WritingTask.INFORMAL_EMAIL: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
            WritingTask.OPINION_ESSAY: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
            WritingTask.LETTER: "please translate the content of this image to text as is written, don`t fix mistakes, Do not take into consideration or transcribe strikedthrough words.",
        }

    def get(self,  task: WritingTask) -> str | None:
        """
        Get the prompt for the given task.
        """
        return self.prompts_mapping.get((task), None)
