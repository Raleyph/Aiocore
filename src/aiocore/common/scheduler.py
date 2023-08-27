import aioschedule
import asyncio


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
