import json
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class JobCreateRequest(BaseModel):
    prompt: str = Field(..., description="The text prompt to generate media from.")
    parameters: str = Field(..., description="Additional parameters for media generation, as a JSON string.")

    class Config:
        from_attributes = True

    @field_validator("parameters", mode="before")
    def parameters_must_be_valid_json(cls, v):
        try:
            json.loads(v)
        except Exception:
            raise ValueError("parameters must be a valid JSON string.")
        return v


class JobStatusResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the job.")
    status: str = Field(..., description="Current status of the job (e.g., queued, running, completed, failed).")
    result_url: Optional[str] = Field(None, description="Path to the generated media file, if available.")
    error: Optional[str] = Field(None, description="Error message if the job failed.")

    class Config:
        from_attributes = True
        populate_by_name = True
