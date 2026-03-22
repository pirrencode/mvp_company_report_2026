"""Streamlit entrypoint for Company Offer Engine."""
from __future__ import annotations

import streamlit as st

from workflow import OfferInput, OfferWorkflow, WorkflowError
from ui import render_output_sections, render_sidebar, render_title


st.set_page_config(
    page_title="Company Offer Engine",
    page_icon="💼",
    layout="wide",
)


def _build_offer_input() -> OfferInput:
    """Render and validate the user input form."""
    st.subheader("Client Discovery Input")
    with st.form("offer_form"):
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Client / Company Name", placeholder="Acme Robotics")
            company_website = st.text_input("Company Website", placeholder="https://acme.com")
            target_service = st.text_input("Target Service to Sell", placeholder="Example: Fractional CTO advisory")
        with col2:
            budget_range = st.text_input("Budget Range", placeholder="$10k - $30k")
            tone_of_voice = st.selectbox(
                "Tone of Voice",
                options=["Consultative", "Executive", "Friendly", "Direct", "Bold"],
                index=0,
            )
        project_brief = st.text_area(
            "Project Brief",
            placeholder="Describe goals, timeline, key stakeholders, current challenge, and desired outcomes.",
            height=180,
        )

        submitted = st.form_submit_button("Generate Offer Pack", use_container_width=True)

    if not submitted:
        raise WorkflowError("Form not submitted yet.", user_facing=False)

    missing = [
        field
        for field, value in {
            "Client / Company Name": client_name,
            "Company Website": company_website,
            "Project Brief": project_brief,
            "Target Service to Sell": target_service,
            "Budget Range": budget_range,
        }.items()
        if not value.strip()
    ]

    if missing:
        raise WorkflowError(f"Please complete the following fields: {', '.join(missing)}")

    return OfferInput(
        client_name=client_name.strip(),
        company_website=company_website.strip(),
        project_brief=project_brief.strip(),
        target_service=target_service.strip(),
        budget_range=budget_range.strip(),
        tone_of_voice=tone_of_voice,
    )


def main() -> None:
    render_sidebar()
    render_title()

    try:
        offer_input = _build_offer_input()
    except WorkflowError as exc:
        if exc.user_facing:
            st.warning(str(exc))
        return

    workflow = OfferWorkflow()

    with st.spinner("Running multi-step agent workflow..."):
        try:
            result = workflow.run(offer_input)
        except WorkflowError as exc:
            st.error(str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            st.error(f"Unexpected error: {exc}")
            return

    render_output_sections(result)


if __name__ == "__main__":
    main()
