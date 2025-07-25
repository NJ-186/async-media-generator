from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Job(SQLModel, table=True):
    __tablename__ = "job"

    id: str = Field(primary_key=True, index=True)
    prompt: str
    parameters: str
    status: str = "queued"
    result_url: Optional[str] = None
    error: Optional[str] = None
    retry_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
