from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import photo_challenge as challenge_crud
from app.crud import guest as guest_crud
from app.crud import photo as photo_crud
from app.schemas.photo_challenge import (
    PhotoChallengeCreate,
    PhotoChallengeResponse,
    ChallengeTaskCreate,
    ChallengeTaskResponse,
    CompletedChallengeTaskCreate,
    ChallengeSummaryResponse,
    PhotoChallengeUpdate,
    ChallengeSummaryGuestResponse
)
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user
from app.schemas.photo import PhotoCreate

router = APIRouter()

@router.post("/", response_model=PhotoChallengeResponse)
async def create_challenge(
    challenge_in: PhotoChallengeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar um novo desafio fotográfico
    """
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=current_user.id)
    if challenge:
        raise HTTPException(status_code=400, detail="Desafio já existe")
    challenge = await challenge_crud.create_photo_challenge(
        db=db,
        challenge_in=challenge_in,
        user_id=current_user.id
    )
    return challenge


@router.get("/", response_model=PhotoChallengeResponse)
async def read_challenge(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obter um desafio específico
    """
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=current_user.id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    if challenge.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este desafio")
    return challenge

@router.put("/", response_model=PhotoChallengeResponse)
async def update_challenge(
    challenge_in: PhotoChallengeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar um desafio específico
    """
    challenge = await challenge_crud.update_photo_challenge_by_user(db=db, user_id=current_user.id, challenge_in=challenge_in)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    if challenge.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este desafio")
    return challenge

@router.delete("/", response_model=PhotoChallengeResponse)
async def delete_challenge(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar um desafio específico
    """
    challenge = await challenge_crud.delete_photo_challenge_by_user(db=db, user_id=current_user.id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    if challenge.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este desafio")
    return challenge

@router.post("/task", response_model=ChallengeTaskResponse)
async def create_task(
    task_in: ChallengeTaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar uma nova tarefa para um desafio
    """
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=current_user.id)
    print(f"Challenge: {challenge.__dict__}")
    print(f"task_in: {task_in.__dict__}")
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    if challenge.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar este desafio")
    
    task = await challenge_crud.create_challenge_task(
        db=db,
        task_in=task_in,
        user_id=current_user.id
    )

    return await challenge_crud.get_challenge_task(db=db, task_id=task.id)

@router.put("/task/{task_id}", response_model=ChallengeTaskResponse)
async def update_task(
    task_id: int,
    task_in: ChallengeTaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar uma tarefa específica
    """
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=current_user.id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    if challenge.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para modificar este desafio")
    
    task = await challenge_crud.update_challenge_task(db=db, task_id=task_id, task_in=task_in, user_id=current_user.id)
    return task

@router.get("/task/{task_id}", response_model=ChallengeTaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obter uma tarefa específica
    """
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=current_user.id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    if challenge.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este desafio")
    
    task = await challenge_crud.get_challenge_task(db=db, task_id=task_id)
    
    if not task or task.challenge_id != challenge.id:
       raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return task


@router.delete("/task/{task_id}", response_model=ChallengeTaskResponse)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar uma tarefa específica
    """
    return await challenge_crud.delete_challenge_task(db=db, task_id=task_id, user_id=current_user.id)


@router.post("/guest/{guest_hash}/task/{task_id}/photo_id/{photo_id}/complete", response_model=ChallengeTaskResponse)
async def complete_task(
    guest_hash: str,
    task_id: int,
    photo_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Marcar uma tarefa como concluída
    """
    # Verificar se a tarefa existe
    task = await challenge_crud.get_challenge_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Verificar se o convidado existe e pertence ao mesmo usuário do desafio
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    album = await photo_crud.get_guest_albums_or_create(db=db, guest_id=guest.id)
    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    if photo.user_id != guest.user_id or photo.photo_album_id != album.id:
        raise HTTPException(status_code=403, detail="Convidado não tem permissão para completar esta tarefa")

    # Verificar se o convidado pertence ao mesmo usuário do desafio
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=guest.user_id)
    if not challenge:
        raise HTTPException(
            status_code=403,
            detail="Convidado não tem permissão para completar esta tarefa"
        )
    
    completed_task = await challenge_crud.get_completed_challenge_task(db=db, task_id=task_id, guest_id=guest.id)
    if completed_task:
        raise HTTPException(status_code=400, detail="Tarefa já completada")
    
    # Criar o objeto CompletedChallengeTaskCreate
    complete_in = CompletedChallengeTaskCreate(
        task_id=task_id,
        photo_id=photo_id,
        guest_id=guest.id
    )
    
    completed_task = await challenge_crud.complete_challenge_task(db=db, complete_in=complete_in)
    if not completed_task:
        raise HTTPException(status_code=400, detail="Não foi possível completar a tarefa")
    
    # Recarregar a tarefa para obter o status atualizado
    updated_task = await challenge_crud.get_challenge_task(db=db, task_id=task_id)
    updated_task.completed_tasks.append(completed_task)
    return updated_task

@router.post("/guest/{guest_hash}/task/{task_id}/with_photo/complete", response_model=ChallengeTaskResponse)
async def complete_task(
    guest_hash: str,
    task_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Marcar uma tarefa como concluída
    """
    # Verificar se a tarefa existe
    task = await challenge_crud.get_challenge_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Verificar se o convidado existe e pertence ao mesmo usuário do desafio
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    album = await photo_crud.get_guest_albums_or_create(db=db, guest_id=guest.id)
    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    

    # Verificar se o convidado pertence ao mesmo usuário do desafio
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=guest.user_id)
    if not challenge:
        raise HTTPException(
            status_code=403,
            detail="Convidado não tem permissão para completar esta tarefa"
        )
    
    completed_task = await challenge_crud.get_completed_challenge_task(db=db, task_id=task_id, guest_id=guest.id)
    if completed_task:
        raise HTTPException(status_code=400, detail="Tarefa já completada")
    
    
    photo = await photo_crud.create_photo(
        db=db,
        photo_in=PhotoCreate(
            user_id=guest.user_id,
            file=file,
            filename=file.filename,
        )
    )

    if not photo:
        raise HTTPException(status_code=400, detail="Não foi possível criar a foto")
    
    await photo_crud.add_photo_to_album(db=db, album_id=album.id, photo_id=photo.id)
    
    completed_task = await challenge_crud.get_completed_challenge_task(db=db, task_id=task_id, guest_id=guest.id)
    if completed_task:
        raise HTTPException(status_code=400, detail="Tarefa já completada")
    
    # Criar o objeto CompletedChallengeTaskCreate
    complete_in = CompletedChallengeTaskCreate(
        task_id=task_id,
        photo_id=photo.id,
        guest_id=guest.id
    )
    
    completed_task = await challenge_crud.complete_challenge_task(db=db, complete_in=complete_in)
    if not completed_task:
        raise HTTPException(status_code=400, detail="Não foi possível completar a tarefa")
    
    # Recarregar a tarefa para obter o status atualizado
    updated_task = await challenge_crud.get_challenge_task(db=db, task_id=task_id)
    updated_task.completed_tasks.append(completed_task)
    return updated_task

@router.put("/guest/{guest_hash}/task/{task_id}/photo_id/{photo_id}/complete", response_model=ChallengeTaskResponse)
async def update_complete_task(
    guest_hash: str,
    task_id: int,
    photo_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Atualizar uma tarefa como concluída
    """
    # Verificar se a tarefa existe
    task = await challenge_crud.get_challenge_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Verificar se o convidado existe e pertence ao mesmo usuário do desafio
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    album = await photo_crud.get_guest_albums_or_create(db=db, guest_id=guest.id)
    if not album:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    if photo.user_id != guest.user_id or photo.photo_album_id != album.id:
        raise HTTPException(status_code=403, detail="Convidado não tem permissão para completar esta tarefa")

    # Verificar se o convidado pertence ao mesmo usuário do desafio
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=guest.user_id)
    if not challenge:
        raise HTTPException(
            status_code=403,
            detail="Convidado não tem permissão para completar esta tarefa"
        )
    
    completed_task = await challenge_crud.get_completed_challenge_task(db=db, task_id=task_id, guest_id=guest.id)
    if not completed_task:
        raise HTTPException(status_code=400, detail="Tarefa não completada")
    
    completed_task.photo_id = photo_id
    db.add(completed_task)
    await db.commit()
    await db.refresh(completed_task)
    
    # Recarregar a tarefa para obter o status atualizado
    updated_task = await challenge_crud.get_challenge_task(db=db, task_id=task_id)
    return updated_task

@router.get("/guest/{guest_hash}/summary", response_model=ChallengeSummaryGuestResponse)
async def get_guest_challenge_summary(
    guest_hash: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Obter um resumo do desafio com tarefas concluídas e pendentes
    """
    print(f"Guest hash: {guest_hash}")
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    print(f"Guest: {guest.__dict__}")
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=guest.user_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    print(f"Challenge: {challenge.__dict__}")
    summary = await challenge_crud.get_challenge_summary_by_guest(db=db, guest_id=guest.id, challenge_id=challenge.id)
    print(f"Summary: {summary.__dict__}")
    if not summary:
        raise HTTPException(status_code=404, detail="Não foi possível gerar o resumo do desafio")
    
    return summary

@router.get("/summary", response_model=ChallengeSummaryResponse)
async def get_challenge_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Obter um resumo do desafio com tarefas concluídas e pendentes
    """
    challenge = await challenge_crud.get_photo_challenge_by_user(db=db, user_id=current_user.id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    if challenge.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem permissão para acessar este desafio")
    
    summary = await challenge_crud.get_challenge_summary(db=db, challenge_id=challenge.id)
    if not summary:
        raise HTTPException(status_code=404, detail="Não foi possível gerar o resumo do desafio")
    
    return summary
