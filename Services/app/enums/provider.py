"""Provider"""
from enum import Enum


class Provider(Enum):
    """
    Enum para los proveedores de modelos de lenguaje.
    """
    AZURE = 'azure'
    OPENAI = 'openai'
    GROQ = 'groq'
    GOOGLE = 'google'
