"""
Handling of content filter errors in LLMs.
"""


class ContentFilterError(Exception):
    """Custom exception for content filter errors in LLMs."""

    def __init__(self, message="The response was blocked by the content filter of the provider."):
        super().__init__(message)
