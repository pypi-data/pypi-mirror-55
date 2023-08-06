import asyncio
import argparse



def main():
    asyncio.run(run())


async def run():
    parser = argparse.ArgumentParser(description='Tea')
    parser.add_argument(
        'task',
        metavar='task',
        type=str,
        choices=['init'],
        help='The task to execute')


    args = parser.parse_args()
    print(args)
    await asyncio.sleep(1)
    print("Tea sample 2")
