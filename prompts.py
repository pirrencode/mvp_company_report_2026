"""Editable prompt templates for Company Offer Engine."""
from __future__ import annotations

SYSTEM_PROMPT = """You are a senior B2B growth strategist and proposal architect.
You produce practical, persuasive deliverables for agency and consulting sales.
Always tailor output to the client context and avoid generic fluff.
"""

WORKFLOW_STEP_PROMPTS = {
    "research": """Analyze the following client context. Infer business model, likely market, current maturity, and strategic priorities.

Return concise bullets with this structure:
- Company Snapshot
- Business Model Signals
- Growth & Market Signals
- Risks / Unknowns

Client context:
{context}
""",
    "pain_points": """Using the research notes below, identify the top 5 likely business pain points relevant to selling this service: {target_service}.

For each pain point include:
- Why it likely exists
- Business impact
- How urgent it may be (Low/Medium/High)

Research:
{research}
""",
    "positioning": """Create a service positioning strategy for {target_service}.

Inputs:
- Client name: {client_name}
- Budget range: {budget_range}
- Tone: {tone_of_voice}
- Pain points:
{pain_points}

Return:
1) Positioning statement (2-3 lines)
2) Offer pillars (3-5 bullets)
3) Proof/credibility angles
4) Objection handling bullets
""",
    "pricing_tiers": """Create 3 pricing tiers for a proposal.

Constraints:
- Align with budget range: {budget_range}
- Service: {target_service}
- Use realistic scope and outcomes

Return exactly 3 tiers:
- Tier name
- Price range
- Deliverables
- Expected outcomes
- Best fit client profile
""",
    "proposal": """Draft a tailored, high-conversion client proposal.

Inputs:
- Client name: {client_name}
- Website: {company_website}
- Brief: {project_brief}
- Service: {target_service}
- Budget: {budget_range}
- Tone: {tone_of_voice}
- Research:
{research}
- Pain points:
{pain_points}
- Positioning:
{positioning}
- Pricing tiers:
{pricing_tiers}

Proposal sections:
1. Executive Summary
2. Current Situation & Opportunity
3. Recommended Approach
4. Scope & Timeline
5. Pricing Options
6. Why Us / Why This Approach
7. Clear Next Steps
""",
    "follow_up": """Write a short follow-up email to send with the proposal.

Inputs:
- Client name: {client_name}
- Tone: {tone_of_voice}
- Proposal summary:
{proposal}

Output:
- Subject line
- Email body (120-180 words)
- CTA sentence
""",
    "qa_refine": """Improve the full offer pack for clarity, persuasion, and executive readability.

Rules:
- Keep claims realistic
- Reduce jargon
- Keep tone consistent
- Preserve structure

Return all sections using markdown H3 headings in this exact order:
### Research
### Pain Points
### Positioning Strategy
### Pricing Tiers
### Tailored Proposal
### Follow-up Email

Content to refine:
{full_content}
""",
}
