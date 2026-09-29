import asyncio
from hindsight_client import Hindsight

async def main():
    client = Hindsight(base_url="http://localhost:8888")

    result = await client.arecall(
        bank_id="revora",
        query="Find previous SaaS deals where implementation cost was an objection and explain what helped them close."
    )

    print("RECALL RESULTS:", len(result.results))

    for item in result.results:
        print("ID:", item.id)
        print("TYPE:", item.type)
        print("TEXT:", item.text)
        print("---")

asyncio.run(main())
