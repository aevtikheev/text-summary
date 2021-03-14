from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import TextSummary


class SummaryPayloadSchema(BaseModel):
    url: str


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


SummarySchema = pydantic_model_creator(TextSummary)
