"""Multi-step agentic workflow orchestration."""
from __future__ import annotations

from dataclasses import dataclass

from llm import LLMClient, LLMConfigurationError
from prompts import SYSTEM_PROMPT, WORKFLOW_STEP_PROMPTS


class WorkflowError(RuntimeError):
    def __init__(self, message: str, *, user_facing: bool = True) -> None:
        super().__init__(message)
        self.user_facing = user_facing


@dataclass
class OfferInput:
    client_name: str
    company_website: str
    project_brief: str
    target_service: str
    budget_range: str
    tone_of_voice: str


@dataclass
class OfferResult:
    research: str
    pain_points: str
    positioning: str
    pricing_tiers: str
    proposal: str
    follow_up_email: str
    refined_pack: str


class OfferWorkflow:
    def __init__(self) -> None:
        try:
            self.llm = LLMClient()
        except LLMConfigurationError as exc:
            raise WorkflowError(str(exc)) from exc

    def _step(self, step_name: str, **kwargs: str) -> str:
        prompt_template = WORKFLOW_STEP_PROMPTS[step_name]
        user_prompt = prompt_template.format(**kwargs)
        try:
            return self.llm.generate(SYSTEM_PROMPT, user_prompt)
        except Exception as exc:  # noqa: BLE001
            raise WorkflowError(f"Model call failed during '{step_name}': {exc}") from exc

    def run(self, offer: OfferInput) -> OfferResult:
        context = (
            f"Client: {offer.client_name}\n"
            f"Website: {offer.company_website}\n"
            f"Project brief: {offer.project_brief}\n"
            f"Target service: {offer.target_service}\n"
            f"Budget range: {offer.budget_range}\n"
            f"Tone: {offer.tone_of_voice}"
        )

        research = self._step("research", context=context)
        pain_points = self._step("pain_points", research=research, target_service=offer.target_service)
        positioning = self._step(
            "positioning",
            client_name=offer.client_name,
            budget_range=offer.budget_range,
            tone_of_voice=offer.tone_of_voice,
            pain_points=pain_points,
            target_service=offer.target_service,
        )
        pricing_tiers = self._step(
            "pricing_tiers",
            budget_range=offer.budget_range,
            target_service=offer.target_service,
        )
        proposal = self._step(
            "proposal",
            client_name=offer.client_name,
            company_website=offer.company_website,
            project_brief=offer.project_brief,
            target_service=offer.target_service,
            budget_range=offer.budget_range,
            tone_of_voice=offer.tone_of_voice,
            research=research,
            pain_points=pain_points,
            positioning=positioning,
            pricing_tiers=pricing_tiers,
        )
        follow_up_email = self._step(
            "follow_up",
            client_name=offer.client_name,
            tone_of_voice=offer.tone_of_voice,
            proposal=proposal,
        )

        combined = (
            f"Research\n{research}\n\n"
            f"Pain Points\n{pain_points}\n\n"
            f"Positioning Strategy\n{positioning}\n\n"
            f"Pricing Tiers\n{pricing_tiers}\n\n"
            f"Tailored Proposal\n{proposal}\n\n"
            f"Follow-up Email\n{follow_up_email}\n"
        )
        refined_pack = self._step("qa_refine", full_content=combined)

        return OfferResult(
            research=research,
            pain_points=pain_points,
            positioning=positioning,
            pricing_tiers=pricing_tiers,
            proposal=proposal,
            follow_up_email=follow_up_email,
            refined_pack=refined_pack,
        )
