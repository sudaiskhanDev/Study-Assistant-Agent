from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):
    batch_size: int = Field(default=3, ge=1, le=10)
    max_retries: int = Field(default=5, ge=0, le=10)


class SummaryResponse(BaseModel):
    summary: str
    source_pages: list[int]
    chunks_processed: int
    batches_completed: int