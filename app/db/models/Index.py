from sqlmodel import SQLModel, Field

class Index(SQLModel, table=True):
    term: str = Field(primary_key=True)
    page: str = Field(primary_key=True)
    freq: int
