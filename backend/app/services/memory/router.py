import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
)

from app.services.memory.memory_service import (
    memory_service,
)


router = APIRouter(
    prefix="/memories",
    tags=["Memories"],
)


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_memory(
    request: MemoryCreate,
    db: AsyncSession = Depends(get_db),
):

    return await memory_service.create_memory(
        db=db,
        user_id=request.user_id,
        key=request.key,
        value=request.value,
    )


@router.get(
    "/user/{user_id}",
    response_model=list[MemoryResponse],
)
async def get_user_memories(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):

    return await memory_service.get_memories_by_user(
        db=db,
        user_id=user_id,
    )


@router.get(
    "/{memory_id}",
    response_model=MemoryResponse,
)
async def get_memory(
    memory_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):

    memory = await memory_service.get_memory(
        db=db,
        memory_id=memory_id,
    )

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail="Memory not found",
        )

    return memory


@router.patch(
    "/{memory_id}",
    response_model=MemoryResponse,
)
async def update_memory(
    memory_id: uuid.UUID,
    request: MemoryUpdate,
    db: AsyncSession = Depends(get_db),
):

    memory = await memory_service.update_memory(
        db=db,
        memory_id=memory_id,
        key=request.key,
        value=request.value,
    )

    if memory is None:
        raise HTTPException(
            status_code=404,
            detail="Memory not found",
        )

    return memory


@router.delete(
    "/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_memory(
    memory_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):

    deleted = await memory_service.delete_memory(
        db=db,
        memory_id=memory_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Memory not found",
        )