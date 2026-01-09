from openai import AzureOpenAI
from resources.AIEngine import AIEngine


class OpenAIAzureEngine(AIEngine):
    def __init__(self, api_version, deployment, api_key):
        super().__init__()
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint="https://mockz.openai.azure.com",
            azure_deployment=deployment
        )
