from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.schemas import SummarySchema, SummaryPayloadSchema, SummaryUpdatePayloadSchema

router = APIRouter()


@router.post('/', response_model=SummarySchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema):
    return await crud.create(payload)


@router.get('/{summary_id}/', response_model=SummarySchema)
async def read_summary(summary_id: int = Path(..., ge=1)):
    summary = await crud.read(summary_id)

    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


@router.get('/', response_model=List[SummarySchema])
async def read_all_summaries():
    return await crud.read_all()


@router.put('/{summary_id}/', response_model=SummarySchema)
async def read_all_summaries(
        payload: SummaryUpdatePayloadSchema,
        summary_id: int = Path(..., ge=1)
):
    summary = await crud.update(summary_id, payload)

    if summary is None:
        raise HTTPException(status_code=404, detail='Summary not found')
    return summary


@router.delete('/{summary_id}/', response_model=SummarySchema)
async def delete_summary(summary_id: int = Path(..., ge=1)) -> SummarySchema:
    summary = await crud.read(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(summary_id)

    return summary
