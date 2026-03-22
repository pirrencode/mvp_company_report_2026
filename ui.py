"""Streamlit UI helpers for output rendering."""
from __future__ import annotations

import streamlit as st

from workflow import OfferResult


def render_title() -> None:
    st.title("💼 Company Offer Engine")
    st.caption(
        "Generate a client-specific strategy, pricing, proposal, and follow-up email using a multi-step AI workflow."
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.header("Settings")
        st.markdown(
            """
**API key loading order**
1. `st.secrets` (recommended for Streamlit Cloud)
2. Environment variable

**Supported providers**
- OpenAI (`LLM_PROVIDER=openai`)
- Anthropic (`LLM_PROVIDER=anthropic`)

You can override models with:
- `OPENAI_MODEL`
- `ANTHROPIC_MODEL`
"""
        )


def _render_section(title: str, content: str) -> None:
    st.markdown(f"### {title}")
    st.code(content, language="markdown")


def render_output_sections(result: OfferResult) -> None:
    st.success("Offer pack generated.")
    tabs = st.tabs(
        [
            "Research",
            "Pain Points",
            "Positioning",
            "Pricing Tiers",
            "Proposal",
            "Follow-up Email",
            "QA Refined Pack",
        ]
    )

    with tabs[0]:
        _render_section("Client Research", result.research)
    with tabs[1]:
        _render_section("Likely Pain Points", result.pain_points)
    with tabs[2]:
        _render_section("Service Positioning Strategy", result.positioning)
    with tabs[3]:
        _render_section("Pricing Tiers", result.pricing_tiers)
    with tabs[4]:
        _render_section("Tailored Proposal", result.proposal)
    with tabs[5]:
        _render_section("Short Follow-up Email", result.follow_up_email)
    with tabs[6]:
        st.markdown("### QA / Refinement Pass")
        st.markdown(result.refined_pack)
