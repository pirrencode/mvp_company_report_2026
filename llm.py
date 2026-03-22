"""LLM provider abstraction for Company Offer Engine."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import streamlit as st


class LLMConfigurationError(RuntimeError):
    """Raised when API credentials or providers are unavailable."""


@dataclass
class LLMConfig:
    provider: str
    model: str
    api_key: str


class LLMClient:
    """Small wrapper around OpenAI or Anthropic chat APIs."""

    def __init__(self) -> None:
        self.config = self._load_config()

    @staticmethod
    def _secret_or_env(secret_name: str, env_name: str) -> Optional[str]:
        if secret_name in st.secrets and st.secrets[secret_name]:
            return str(st.secrets[secret_name])
        return os.getenv(env_name)

    def _load_config(self) -> LLMConfig:
        provider = self._secret_or_env("LLM_PROVIDER", "LLM_PROVIDER") or "openai"
        provider = provider.lower().strip()

        if provider == "openai":
            api_key = self._secret_or_env("OPENAI_API_KEY", "OPENAI_API_KEY")
            model = self._secret_or_env("OPENAI_MODEL", "OPENAI_MODEL") or "gpt-4.1-mini"
        elif provider == "anthropic":
            api_key = self._secret_or_env("ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")
            model = self._secret_or_env("ANTHROPIC_MODEL", "ANTHROPIC_MODEL") or "claude-3-5-sonnet-latest"
        else:
            raise LLMConfigurationError(
                "Unsupported provider. Set LLM_PROVIDER to 'openai' or 'anthropic'."
            )

        if not api_key:
            raise LLMConfigurationError(
                f"Missing API key for {provider}. Set it in .streamlit/secrets.toml or environment variables."
            )

        return LLMConfig(provider=provider, model=model, api_key=api_key)

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
        if self.config.provider == "openai":
            from openai import OpenAI

            client = OpenAI(api_key=self.config.api_key)
            response = client.responses.create(
                model=self.config.model,
                temperature=temperature,
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.output_text.strip()

        if self.config.provider == "anthropic":
            from anthropic import Anthropic

            client = Anthropic(api_key=self.config.api_key)
            message = client.messages.create(
                model=self.config.model,
                max_tokens=1800,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            parts = [block.text for block in message.content if hasattr(block, "text")]
            return "\n".join(parts).strip()

        raise LLMConfigurationError(f"Unknown provider: {self.config.provider}")
