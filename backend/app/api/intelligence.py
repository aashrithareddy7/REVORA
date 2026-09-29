from fastapi import APIRouter
from app.hindsight.memory import recall_similar_deals
from app.agent.reasoner import analyze_deal

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])


@router.get("/analyze")
async def analyze(
    company: str,
    industry: str,
    stage: str,
    value: float,
    objection: str,
):
    memories_response = await recall_similar_deals(
        industry=industry,
        stage=stage,
        objection=objection,
    )

    memories = memories_response.results

    recommendation = await analyze_deal(
        company=company,
        industry=industry,
        stage=stage,
        value=value,
        objection=objection,
        memories=memories,
    )

    return {
        "deal": {
            "company": company,
            "industry": industry,
            "stage": stage,
            "value": value,
            "objection": objection,
        },
        "memory_source": "Hindsight",
        "memory_count": len(memories),
        "historical_evidence": [
            {
                "id": item.id,
                "type": item.type,
                "text": item.text,
            }
            for item in memories
        ],
        "ai_recommendation": recommendation,
    }
