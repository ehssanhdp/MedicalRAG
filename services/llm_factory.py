from typing import Any, Dict, List
from groq import Groq
from config.settings import get_settings


class LLMFactory:
    """Factory class for creating and managing LLM interactions using the Groq API."""

    def __init__(self):
        """Initialize the LLMFactory with a Groq client and load settings."""
        self.client = Groq()
        self.settings = get_settings().LLAMA 

    def create_completion(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Any:
        """
        Create a chat completion using the Groq API.
        
        Args:
            response_model (Type): The model used to parse the response.
            messages (List[Dict[str, str]]): List of messages in the chat history.
            **kwargs: Additional parameters to override default settings.

        Returns:
            Any: The Groq API response.
        """
        # Combine default settings with kwargs
        completion_params = {
            "model": kwargs.get("model", self.settings.default_model),
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
            "messages": messages,
            "top_p": kwargs.get("max_retries", self.settings.top_p),
            "stream": kwargs.get("max_retries", self.settings.stream),
            "stop": kwargs.get("max_retries", self.settings.stop), 
        }

        return self.client.chat.completions.create(**completion_params)
