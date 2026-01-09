"""Config"""
import json

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from app.core.base_config import BaseConfig


# Cargar variables de entorno desde .env
load_dotenv(override=True, dotenv_path='./config/.env')


class AppSettings(BaseConfig):
    """AppSettings class."""
    model_config = SettingsConfigDict(env_prefix="APP_")
    LOG_LEVEL: str = Field(default="ERROR")
    PROCESSING_THREADS: int = Field(default=5)
    FRONTEND_URL: str = Field(...)


class AWSConfig(BaseConfig):
    """AWSConfig class."""
    model_config = SettingsConfigDict(env_prefix="AWS_")
    REGION: str = Field(...)
    ACCESS_KEY_ID: str = Field(...)
    SECRET_ACCESS_KEY: str = Field(...)


class SQSSettings(BaseConfig):
    """SQSSettings class."""
    model_config = SettingsConfigDict(env_prefix="SQS_")
    QUEUE_URL: str = Field(...)
    VISIBILITY_TIMEOUT: int = Field(default=30)
    WAIT_TIME: int = Field(default=20)
    MAX_MESSAGES: int = Field(default=10)


class MongoSettings(BaseConfig):
    """MongoSettings class."""
    model_config = SettingsConfigDict(env_prefix="MONGO_")
    DATABASE: str = Field(...)
    TEST_DATABASE: str = Field(...)
    URL: str = Field(...)
    TEST_URI: str = Field(...)


class OpenAISettings(BaseConfig):
    """OpenAISettings class."""
    model_config = SettingsConfigDict(env_prefix="OPENAI_")
    API_KEY: str = Field(...)
    ENDPOINT: str = Field(...)
    CHAT_DEPLOYMENT_NAME: str = Field(...)
    CHAT_API_VERSION: str = Field(...)
    MINI_DEPLOYMENT_NAME: str = Field(...)
    MINI_API_VERSION: str = Field(...)
    CHAT_DEPLOYMENT_NAME_41: str = Field(...)
    CHAT_API_VERSION_41: str = Field(...)
    MINI_DEPLOYMENT_NAME_41: str = Field(...)
    MINI_API_VERSION_41: str = Field(...)


class GroqSettings(BaseConfig):
    """GroqSettings class."""
    model_config = SettingsConfigDict(env_prefix="GROQ_")
    API_KEY: str = Field(...)


class GoogleSettings(BaseConfig):
    """GoogleSettings class."""
    model_config = SettingsConfigDict(env_prefix="GOOGLE_")
    API_KEY: str = Field(...)


class LangsmithSettings(BaseConfig):
    """LangsmithSettings class."""
    model_config = SettingsConfigDict(env_prefix="LANGSMITH_")
    TRACING: str = Field(default="false")
    ENDPOINT: str = Field(...)
    API_KEY: str = Field(...)
    PROJECT: str = Field(...)


class StripeSettings(BaseConfig):
    """StripeSettings class."""
    model_config = SettingsConfigDict(env_prefix="STRIPE_")
    SECRET_KEY: str = Field(...)
    SIGNING_SECRET_DE_WEBHOOK: str = Field(...)
    PAYMENTS_ENDPOINT: str = Field(...)


class AuthSettings(BaseConfig):
    """AuthSettings class."""
    model_config = SettingsConfigDict(env_prefix="AUTH_")
    SECRET_KEY: str = Field(...)
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=90)
    ADMIN_EMAIL: str = Field(...)
    ADMIN_PASSWORD: str = Field(...)


class EmailSettings(BaseConfig):
    """EmailSettings class."""
    model_config = SettingsConfigDict(env_prefix="EMAIL_")
    MAIL_USER_INFO: str = Field(...)
    MAIL_PASS_INFO: str = Field(...)
    CAPTCHA_PRIVATE_KEY: str = Field(...)


class OAuthSettings(BaseConfig):
    """OAuthSettings class."""
    model_config = SettingsConfigDict(env_prefix="OAUTH_")
    GOOGLE_CLIENT_ID: str = Field(...)
    MICROSOFT_CLIENT_ID: str = Field(...)
    MICROSOFT_TENANT_ID: str = Field(...)


class S3Settings(BaseConfig):
    """S3Settings class."""
    model_config = SettingsConfigDict(env_prefix="S3_")
    BUCKET_NAME: str = Field(...)
    IMAGE_STORAGE_PROVIDER: str = Field(default="S3")


def mask_secrets(data: dict, keys_to_mask: set[str] = None) -> dict:
    """Mask secrets in the data."""
    keys_to_mask = keys_to_mask or {
        "SECRET_KEY", "SECRET_ACCESS_KEY", "ACCESS_KEY_ID", "SESSION_TOKEN",
        "STRIPE_SECRET_KEY", "ADMIN_PASSWORD", "MAIL_PASS", "MAIL_PASS_INFO",
        "CAPTCHA_PRIVATE_KEY", "API_KEY", "SIGNING_SECRET_DE_WEBHOOK"
    }
    return {
        key: "***" if key in keys_to_mask else value
        for key, value in data.items()
    }


class Settings:
    """Settings class."""
    app = AppSettings()
    aws = AWSConfig()
    sqs = SQSSettings()
    mongo = MongoSettings()
    openai = OpenAISettings()
    groq = GroqSettings()
    google = GoogleSettings()
    langsmith = LangsmithSettings()
    stripe = StripeSettings()
    auth = AuthSettings()
    email = EmailSettings()
    oauth = OAuthSettings()
    s3 = S3Settings()

    def __init__(self):
        self.app = AppSettings()
        self.aws = AWSConfig()
        self.sqs = SQSSettings()
        self.mongo = MongoSettings()
        self.openai = OpenAISettings()
        self.groq = GroqSettings()
        self.google = GoogleSettings()
        self.langsmith = LangsmithSettings()
        self.stripe = StripeSettings()
        self.auth = AuthSettings()
        self.email = EmailSettings()
        self.oauth = OAuthSettings()
        self.s3 = S3Settings()

    def model_dump(self, should_mask_secrets: bool = True):
        """Dump the settings, optionally masking secrets."""
        data = {
            "app": self.app.model_dump(),
            "aws": self.aws.model_dump(),
            "sqs": self.sqs.model_dump(),
            "mongo": self.mongo.model_dump(),
            "openai": self.openai.model_dump(),
            "groq": self.groq.model_dump(),
            "google": self.google.model_dump(),
            "langsmith": self.langsmith.model_dump(),
            "stripe": self.stripe.model_dump(),
            "auth": self.auth.model_dump(),
            "email": self.email.model_dump(),
            "oauth": self.oauth.model_dump(),
            "s3": self.s3.model_dump()
        }

        if should_mask_secrets:
            return {k: mask_secrets(v) for k, v in data.items()}

        return json.dumps(data, indent=4)


settings = Settings()
