from abc import ABC, abstractmethod


class IAIService(ABC):
    def __init__(self):
        self._model_audio = "whisper-1"
        self._model_text = "gpt-4o"
        self._model_embeddings = "text-embedding-3-small"
        self._max_tokens = 2000
        self._temperature = 0.7

    @property
    def model_audio(self) -> str:
        return self._model_audio

    @model_audio.setter
    def model_audio(self, value: str):
        self._model_audio = value

    @property
    def model_text(self) -> str:
        return self._model_text

    @model_text.setter
    def model_text(self, value: str):
        self._model_text = value

    @property
    def model_embeddings(self) -> str:
        return self._model_embeddings

    @model_embeddings.setter
    def model_embeddings(self, value: str):
        self._model_embeddings = value

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value: int):
        self._max_tokens = value

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float):
        self._temperature = value

    @abstractmethod
    def parse(self, output_model, prompt: dict[str, str]):
        pass
