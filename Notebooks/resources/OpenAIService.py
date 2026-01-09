import logging

from resources.AIEngine import AIEngine
from resources.IAiService import IAIService


class OpenAIService(IAIService):

    def __init__(self, engine_text: AIEngine):
        super().__init__()
        self.engine_text = engine_text

    def parse(self, output_model, prompt: dict[str, str]):
        completion = self.engine_text.client.beta.chat.completions.parse(
            model=self.model_text,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=prompt,
            response_format=output_model,

        )
        logging.info(f"Text Tokens Usage: {completion.usage.total_tokens}")

        # If the model refuses to respond, you will get a refusal message
        if (completion.choices[0].message.refusal):
            logging.info(completion.choices[0].message.refusal)
        else:
            logging.info(completion.choices[0].message.parsed)

        return completion.choices[0].message.parsed, completion.usage.total_tokens

    def predict(self, prompt: list[dict[str, str]]):
        completion = self.engine_text.client.chat.completions.create(
            model=self.model_text,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"},
            temperature=self.temperature,
            messages=prompt,
        )
        logging.info(f"Text Tokens Usage: {completion.usage.total_tokens}")

        return completion.choices[0].message.content, completion.usage.total_tokens