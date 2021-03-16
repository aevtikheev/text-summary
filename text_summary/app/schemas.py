from pydantic import BaseModel, AnyHttpUrl
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import TextSummary


class SummaryPayloadSchema(BaseModel):
    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str


SummarySchema = pydantic_model_creator(TextSummary)
