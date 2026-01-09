"""Deployment"""
from enum import Enum


class Deployment(Enum):
    """
    Enum para los deployments de modelos de lenguaje.
    """
    GPT_4O = 'gpt-4o'
    GPT_4O_MINI = 'gpt-4o-mini'
    LLAMA4 = 'meta-llama/llama-4-scout-17b-16e-instruct'
    GPT_41 = 'gpt-4.1'
    GPT_41_MINI = 'gpt-4.1-mini'
    GEMINI_2_5_FLASH = 'gemini-2.5-flash-preview-04-17'
