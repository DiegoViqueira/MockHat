"""Debug Messages Handler"""
from typing import Any, Dict, List

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import BaseMessage, LLMResult


class DebugMessagesHandler(BaseCallbackHandler):
    """
    A callback handler that prints the messages in a readable format.
    """

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        pass

    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs: Any) -> Any:
        """Run when Chat Model starts running."""
        pass

        # for message in messages:
        #     for msg in message:
        #         msg.pretty_print()

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        pass
