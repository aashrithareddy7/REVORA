from app.database import engine, Base
from app.models.deal import Deal
from app.models.outcome import DealOutcome


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
