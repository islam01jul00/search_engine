# load_index.py

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import select
from app.db.models import Index
from app.db import AsyncSessionLocal, sync_engine 


async def load_index(file_path: str):
    # Step 1: Create tables using the sync engine
    SQLModel.metadata.create_all(sync_engine)

    # Step 2: Load data using async session
    async with AsyncSessionLocal() as session:
        with open(file_path, "r") as file:
            for line in file:
                if "=>" not in line:
                    continue

                term, data = line.strip().split("=>", 1)
                term = term.strip()
                entries = data.strip().split(";")

                for entry in entries:
                    entry = entry.strip()

                    if entry.startswith("total") or ":" not in entry:
                        continue

                    page, freq = entry.split(":")
                    exesting_record = await session.execute(select(Index).where(Index.term == term, Index.page == page.strip()))
                    exesting_record = exesting_record.scalars().first()

                    if exesting_record:
                        exesting_record.freq = int(freq.strip())
                        session.add(exesting_record)

                        continue

                    record = Index(term=term, page=page.strip(), freq=int(freq.strip()))

                    session.add(record)

        await session.commit()
        print("Index loaded successfully.")