import os

from app.hindsight.client import client

BANK_ID = os.environ["HINDSIGHT_BANK_ID"]


async def retain_deal_experience(
    company: str,
    industry: str,
    stage: str,
    value: float,
    objection: str,
    outcome: str,
    lesson: str,
):
    content = (
        f"Revenue deal experience: Company={company}; "
        f"Industry={industry}; Stage={stage}; Value=${value:,.0f}; "
        f"Objection={objection}; Outcome={outcome}; Lesson={lesson}."
    )

    return await client.aretain(
        bank_id=BANK_ID,
        content=content,
        context="REVORA sales/revenue deal experience",
        metadata={
            "company": company,
            "industry": industry,
            "stage": stage,
            "outcome": outcome,
        },
        tags=["revenue", "deal", outcome.lower()],
    )


async def recall_similar_deals(
    industry: str,
    stage: str,
    objection: str,
):
    query = (
        f"Find historical revenue deals similar to this opportunity: "
        f"industry={industry}, stage={stage}, objection={objection}. "
        f"Focus on previous outcomes, successful approaches, failures, "
        f"and lessons learned."
    )

    return await client.arecall(
        bank_id=BANK_ID,
        query=query,
    )
