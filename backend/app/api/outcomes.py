from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.deal import Deal
from app.models.outcome import DealOutcome
from app.hindsight.memory import retain_deal_experience

router = APIRouter(prefix="/outcomes", tags=["Outcomes"])


@router.post("/")
async def record_outcome(
    deal_id: int,
    outcome: str,
    lesson: str,
    db: AsyncSession = Depends(get_db),
):
    deal = await db.get(Deal, deal_id)

    if not deal:
        return {
            "error": "Deal not found",
            "deal_id": deal_id,
        }

    outcome_record = DealOutcome(
        deal_id=deal_id,
        outcome=outcome.upper(),
        lesson=lesson,
    )

    deal.status = outcome.upper()

    db.add(outcome_record)
    await db.commit()
    await db.refresh(outcome_record)

    await retain_deal_experience(
        company=deal.company,
        industry=deal.industry,
        stage=deal.stage,
        value=deal.value,
        objection=deal.objection,
        outcome=outcome.upper(),
        lesson=lesson,
    )

    return {
        "success": True,
        "deal_id": deal_id,
        "outcome": outcome.upper(),
        "lesson": lesson,
        "memory_source": "Hindsight",
        "message": "Outcome recorded and new lesson retained in Hindsight.",
    }
