from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import TextSummary


class SummaryPayloadSchema(BaseModel):
    url: str


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


SummarySchema = pydantic_model_creator(TextSummary)
