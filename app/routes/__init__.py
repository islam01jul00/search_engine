from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import engine
from app.db.models import Index

router = APIRouter(prefix="/search")

@router.get("/")
async def search(request: Request):
    term = request.query_params.get("term")
    if not term:
        raise HTTPException(status_code=400, detail="Term is required")

    async with AsyncSession(engine) as session:
        statement = select(Index).where(Index.term == term).order_by(Index.freq.desc())
        results = await session.execute(statement)
        rows = results.scalars().all()

    response = {
        "term": term,
        "results": [
            {
                "page": row.page,
                "freq": row.freq
            }
            for row in rows
        ],
        "total_occurrences": sum(row.freq for row in rows),
        "total_documents": len(rows)
    }

    for result in response["results"]:
        page_id = result["page"]

        try:
            filename = f"data/pages/page_{page_id.replace('p', '')}.txt"
            print(f"Opening file: {filename}")

            with open(filename, "r") as f:
                url_line = f.readline().strip()
                print(f"Read URL line: {url_line}")

                result["page"] = {
                    "id": page_id,
                    "url": url_line.removeprefix("URL:").strip() if url_line.startswith("URL:") else url_line
                }

        except Exception as e:
            print(f"Error processing file {filename}: {e}")
            result["page"] = {
                "id": page_id,
                "url": None,
                "error": str(e)
            }

    return JSONResponse(response)