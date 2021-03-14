from typing import List

from fastapi import APIRouter, HTTPException

from app.api import crud
from app.schemas import SummarySchema, SummaryPayloadSchema, SummaryUpdatePayloadSchema

router = APIRouter()


@router.post('/', response_model=SummarySchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema):
    return await crud.create(payload)


@router.get('/{id_}/', response_model=SummarySchema)
async def read_summary(id_: int):
    summary = await crud.read(id_)

    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


@router.get('/', response_model=List[SummarySchema])
async def read_all_summaries():
    return await crud.read_all()


@router.put('/{id_}/', response_model=SummarySchema)
async def read_all_summaries(id_: int, payload: SummaryUpdatePayloadSchema):
    summary = await crud.update(id_, payload)

    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


@router.delete('/{id_}/', response_model=SummarySchema)
async def delete_summary(id_: int) -> SummarySchema:
    summary = await crud.read(id_)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(id_)

    return summary
