from typing import List, Optional

from app.schemas import SummaryPayloadSchema, SummaryUpdatePayloadSchema
from app.models import TextSummary


async def create(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary='')
    await summary.save()

    return summary.id


async def read(id_: int) -> Optional[dict]:
    summary = await TextSummary.filter(id=id_).first().values()

    return summary[0] if summary else None


async def read_all() -> List:
    return await TextSummary.all().values()


async def update(id_: int, payload: SummaryUpdatePayloadSchema) -> Optional[dict]:
    summary = await TextSummary.filter(id=id_).first().update(
        url=payload.url, summary=payload.summary,
    )
    if summary:
        updated_summary = await TextSummary.filter(id=id_).first().values()
        return updated_summary[0]
    return None


async def delete(id_: int) -> Optional[dict]:
    return await TextSummary.filter(id=id_).first().delete()
