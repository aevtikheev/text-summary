from typing import List

from fastapi import APIRouter, HTTPException

from app.api import crud
from app.schemas import SummarySchema, SummaryPayloadSchema, SummaryResponseSchema

router = APIRouter()


@router.post('/', response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema):
    summary_id = await crud.create(payload)

    return {
        'id': summary_id,
        'url': payload.url,
    }


@router.get('/{id_}/', response_model=SummarySchema)
async def read_summary(id_: int):
    summary = await crud.read(id_)

    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


@router.get('/', response_model=List[SummarySchema])
async def read_all_summaries():
    return await crud.read_all()
