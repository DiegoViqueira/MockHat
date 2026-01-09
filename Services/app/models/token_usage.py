"""Model Token Usage"""
from pydantic import BaseModel, Field


class TokensUsage(BaseModel):
    """Model for storing tokens usage information."""
    prompt_tokens: int = Field(0, description="")
    completion_tokens: int = Field(0, description="")
    total_tokens: int = Field(0, description="")
    total_cost: float = Field(0, description="Total cost in USD")
    cached_tokens: int = Field(0, description="")
    reasoning_tokens: int = Field(0, description="")

    def __add__(self, other):
        return TokensUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
            total_cost=self.total_cost + other.total_cost,
        )
