import asyncio

from scripts import load_index

if __name__ == "__main__":
    asyncio.run(load_index("data/index.txt"))
