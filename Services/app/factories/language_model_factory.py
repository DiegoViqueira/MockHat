"""Language Model Factory"""

from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.settings import settings
from app.enums.deployment import Deployment
from app.enums.provider import Provider


class ModelEngine:
    """
    Engine para crear modelos de lenguaje.
    """

    def __init__(self, model: ChatGroq | AzureChatOpenAI, provider: Provider, deployment: Deployment):
        self.model = model
        self.provider = provider
        self.deployment = deployment


class LanguageModelFactory:
    """
    Factory para crear modelos de lenguaje.
    """
    @staticmethod
    def create_model(provider: Provider, deployment: Deployment, temperature: float = 0.1, max_tokens: int = 32768):
        """
        Crea un modelo de lenguaje según el proveedor y el nombre del deployment.
        """
        if provider == Provider.AZURE:
            if deployment == Deployment.GPT_4O:
                return ModelEngine(
                    model=AzureChatOpenAI(
                        api_key=settings.openai.API_KEY,
                        azure_endpoint=settings.openai.ENDPOINT,
                        azure_deployment=settings.openai.CHAT_DEPLOYMENT_NAME,
                        openai_api_version=settings.openai.CHAT_API_VERSION,
                        temperature=temperature,
                        max_tokens=max_tokens if max_tokens <= 32768 else 32768),
                    provider=provider,
                    deployment=deployment
                )
            elif deployment == Deployment.GPT_4O_MINI:
                return ModelEngine(
                    model=AzureChatOpenAI(
                        api_key=settings.openai.API_KEY,
                        azure_endpoint=settings.openai.ENDPOINT,
                        azure_deployment=settings.openai.MINI_DEPLOYMENT_NAME,
                        openai_api_version=settings.openai.MINI_API_VERSION,
                        temperature=temperature,
                        max_tokens=max_tokens if max_tokens <= 32768 else 32768),
                    provider=provider,
                    deployment=deployment
                )
            elif deployment == Deployment.GPT_41:
                return ModelEngine(
                    model=AzureChatOpenAI(
                        api_key=settings.openai.API_KEY,
                        azure_endpoint=settings.openai.ENDPOINT,
                        azure_deployment=settings.openai.CHAT_DEPLOYMENT_NAME_41,
                        openai_api_version=settings.openai.CHAT_API_VERSION_41,
                        temperature=temperature,
                        max_tokens=max_tokens if max_tokens <= 32768 else 32768),
                    provider=provider,
                    deployment=deployment
                )
            elif deployment == Deployment.GPT_41_MINI:
                return ModelEngine(
                    model=AzureChatOpenAI(
                        api_key=settings.openai.API_KEY,
                        azure_endpoint=settings.openai.ENDPOINT,
                        azure_deployment=settings.openai.MINI_DEPLOYMENT_NAME_41,
                        openai_api_version=settings.openai.MINI_API_VERSION_41,
                        temperature=temperature,
                        max_tokens=max_tokens if max_tokens <= 32768 else 32768),
                    provider=provider,
                    deployment=deployment
                )
            else:
                raise ValueError(
                    f"Deployment '{deployment.value}' no soportado.")

        elif provider == Provider.GROQ:
            if deployment == Deployment.LLAMA4:
                return ModelEngine(
                    model=ChatGroq(
                        model=deployment.value,
                        api_key=settings.groq.API_KEY,
                        temperature=temperature,
                        max_tokens=max_tokens if max_tokens <= 8191 else 8191
                    ),
                    provider=provider,
                    deployment=deployment
                )
            else:
                raise ValueError(
                    f"Deployment '{deployment.value}' not supported for Groq.")

        elif provider == Provider.GOOGLE:
            if deployment == Deployment.GEMINI_2_5_FLASH:
                return ModelEngine(
                    model=ChatGoogleGenerativeAI(
                        model=deployment.value,
                        api_key=settings.google.API_KEY,
                        temperature=temperature,
                        max_tokens=max_tokens if max_tokens <= 8191 else 8191
                    ),
                    provider=provider,
                    deployment=deployment
                )
            else:
                raise ValueError(
                    f"Deployment '{deployment.value}' not supported for Google.")
        else:
            raise ValueError(
                f"Proveedor de modelo '{provider.value}' no soportado.")
