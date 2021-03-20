"""Pydantic schemes for summarizer app."""
from pydantic import BaseModel, AnyHttpUrl
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import TextSummary


class SummaryPayloadSchema(BaseModel):
    """Schema of the request for creating a summary."""
    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    """Schema of the response for creating a summary."""
    id: int  # noqa: VNE003


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    """Schema of the request for updating a summary."""
    summary: str


SummarySchema = pydantic_model_creator(TextSummary)
