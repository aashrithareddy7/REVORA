from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.deal import Deal
from app.hindsight.memory import retain_deal_experience

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.post("/")
async def create_deal(
    company: str,
    industry: str,
    stage: str,
    value: float,
    objection: str,
    db: AsyncSession = Depends(get_db),
):
    deal = Deal(
        company=company,
        industry=industry,
        stage=stage,
        value=value,
        objection=objection,
    )

    db.add(deal)
    await db.commit()
    await db.refresh(deal)

    await retain_deal_experience(
        company=company,
        industry=industry,
        stage=stage,
        value=value,
        objection=objection,
        outcome="OPEN",
        lesson="New opportunity entered the REVORA pipeline.",
    )

    return {
        "id": deal.id,
        "company": deal.company,
        "industry": deal.industry,
        "stage": deal.stage,
        "value": deal.value,
        "objection": deal.objection,
        "status": deal.status,
        "memory": "Hindsight experience retained",
    }


@router.get("/")
async def list_deals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Deal).order_by(Deal.id.desc())
    )

    deals = result.scalars().all()

    return [
        {
            "id": deal.id,
            "company": deal.company,
            "industry": deal.industry,
            "stage": deal.stage,
            "value": deal.value,
            "objection": deal.objection,
            "status": deal.status,
        }
        for deal in deals
    ]
