from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    pdf_name: str
    total_pages: int
    total_chunks: int