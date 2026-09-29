import asyncio
from hindsight_client import Hindsight

async def main():
    client = Hindsight(base_url="http://localhost:8888")

    result = await client.aretain(
        bank_id="revora",
        content="Acme Analytics is a SaaS deal worth $85,000 in Negotiation. The customer objected to implementation cost. Outcome: WON. Lesson: A phased implementation pilot reduced implementation-cost concerns and helped close the deal.",
        context="REVORA revenue deal experience",
        metadata={
            "company": "Acme Analytics",
            "industry": "SaaS",
            "stage": "Negotiation",
            "outcome": "WON"
        },
        tags=["revenue", "deal", "won"]
    )

    print("MEMORY RETAINED")
    print(result)

asyncio.run(main())
