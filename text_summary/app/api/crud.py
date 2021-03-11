from typing import List, Optional

from app.schemas import SummaryPayloadSchema
from app.models import TextSummary


async def create(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(url=payload.url, summary='dummy summary')
    await summary.save()

    return summary.id


async def read(id_: int) -> Optional[dict]:
    summary = await TextSummary.filter(id=id_).first().values()

    return summary[0] if summary else None


async def read_all() -> List:
    summaries = await TextSummary.all().values()
    return summaries
