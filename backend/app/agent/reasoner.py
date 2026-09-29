import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])


async def analyze_deal(
    company: str,
    industry: str,
    stage: str,
    value: float,
    objection: str,
    memories: list,
):
    evidence = "\n\n".join(
        f"- {item.text}"
        for item in memories
    )

    prompt = f"""
You are REVORA, an AI Revenue Memory Engine.

Your job is to analyze a current sales opportunity using historical
experiences recalled from Hindsight.

CURRENT DEAL
Company: {company}
Industry: {industry}
Stage: {stage}
Deal Value: ${value:,.0f}
Objection: {objection}

HINDSIGHT HISTORICAL EVIDENCE
{evidence}

Based ONLY on the historical evidence and current deal information,
produce a practical sales recommendation.

Return exactly these sections:

RECOMMENDATION:
What should the sales team do next?

WHY:
Explain the reasoning using historical evidence.

RISK:
What could cause this deal to fail?

NEXT_ACTION:
Give one concrete action the salesperson should take.

CONFIDENCE:
Give a confidence level from 0 to 100 based on the strength and
relevance of the recalled evidence.

IMPORTANT:
Do not invent historical deals or evidence.
If evidence is weak, explicitly say so.
"""

    response = await client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are REVORA's revenue intelligence reasoning engine."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
