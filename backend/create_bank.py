import asyncio
from hindsight_client import Hindsight

async def main():
    client = Hindsight(base_url="http://localhost:8888")
    await client.acreate_bank(
        bank_id="revora",
        name="REVORA Revenue Memory",
    )
    print("BANK CREATED")

asyncio.run(main())
