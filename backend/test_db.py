import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        "postgresql://revora:revora@127.0.0.1:5432/revora"
    )
    print("POSTGRESQL CONNECTION: OK")
    await conn.close()

asyncio.run(test())
