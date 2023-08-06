import asyncio

def main():
    asyncio.run(run())


async def run():
    await asyncio.sleep(1)
    print("Tea sample 2")
