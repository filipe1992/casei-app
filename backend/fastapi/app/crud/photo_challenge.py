from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists, select, func
from sqlalchemy.orm import joinedload
from collections import defaultdict

from app.models.photo_challenge import PhotoChallenge, ChallengeTask, CompletedChallengeTask
from app.schemas.photo_challenge import ChallengeSummaryGuestResponse, ChallengeTaskResponse, ChallengeTaskResponseGuest, PhotoChallengeCreate, ChallengeTaskCreate, CompletedChallengeTaskCreate, PhotoChallengeUpdate
from app.errors.base import create_not_found_error, ErrorCode

# PhotoChallenge CRUD
async def create_photo_challenge(
    db: AsyncSession,
    challenge_in: PhotoChallengeCreate,
    user_id: int
) -> PhotoChallenge:
    db_challenge = PhotoChallenge(
        title=challenge_in.title,
        user_id=user_id
    )
    db.add(db_challenge)
    await db.commit()
    await db.refresh(db_challenge)
    return await get_photo_challenge_by_user(db=db, user_id=user_id)

async def get_photo_challenge_by_user(
    db: AsyncSession,
    user_id: int
) -> Optional[PhotoChallenge]:
    stmt = (
        select(PhotoChallenge)
        .options(
            joinedload(PhotoChallenge.tasks)
            .joinedload(ChallengeTask.completed_tasks)
            .joinedload(CompletedChallengeTask.guest)
        )
        .where(PhotoChallenge.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.unique().scalar_one_or_none()

async def update_photo_challenge_by_user(
    db: AsyncSession,
    user_id: int,
    challenge_in: PhotoChallengeUpdate
) -> PhotoChallenge:
    challenge = await get_photo_challenge_by_user(db=db, user_id=user_id)
    print(challenge)
    if not challenge:
        raise create_not_found_error(
            error_code=ErrorCode.NOT_FOUND,
            message="Desafio não encontrado",
            validation_errors=[]
        )
    
    challenge.title = challenge_in.title
    db.add(challenge)
    await db.commit()
    await db.refresh(challenge)
    return challenge

async def delete_photo_challenge_by_user(
    db: AsyncSession,
    user_id: int
) -> PhotoChallenge:
    challenge = await get_photo_challenge_by_user(db=db, user_id=user_id)
    if not challenge:
        raise create_not_found_error(
            error_code=ErrorCode.NOT_FOUND,
            message="Desafio não encontrado",
            validation_errors=[]
        )
    
    await db.delete(challenge)
    await db.commit()
    return challenge   

# ChallengeTask CRUD
async def create_challenge_task(
    db: AsyncSession,
    task_in: ChallengeTaskCreate,
    user_id: int
) -> ChallengeTask:
    challenge = await get_photo_challenge_by_user(db=db, user_id=user_id)
    if not challenge:
        raise create_not_found_error(
            error_code=ErrorCode.NOT_FOUND,
            message="Desafio não encontrado",
            validation_errors=[]
        )
    
    db_task = ChallengeTask(
        title=task_in.title,
        description=task_in.description,
        challenge_id=challenge.id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_challenge_task(
    db: AsyncSession,
    task_id: int,
    task_in: ChallengeTaskCreate,
    user_id: int
) -> ChallengeTask:
    challenge = await get_photo_challenge_by_user(db=db, user_id=user_id)
    if not challenge:
        raise create_not_found_error(
            error_code=ErrorCode.NOT_FOUND,
            message="Desafio não encontrado",
            validation_errors=[]
        )

    task = await get_challenge_task(db=db, task_id=task_id)
    if not task or task.challenge_id != challenge.id:
        raise create_not_found_error(
            error_code=ErrorCode.NOT_FOUND,
            message="Tarefa não encontrada",
            validation_errors=[]
        )

    task.title = task_in.title
    task.description = task_in.description
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def delete_challenge_task(
    db: AsyncSession,
    task_id: int,
    user_id: int
) -> ChallengeTask:
    challenge = await get_photo_challenge_by_user(db=db, user_id=user_id)
    if not challenge:
        raise create_not_found_error(
            error_code=ErrorCode.NOT_FOUND,
            message="Desafio não encontrado",
            validation_errors=[]
        )

    task = await get_challenge_task(db=db, task_id=task_id)
    if not task or task.challenge_id != challenge.id:
        raise create_not_found_error(
            error_code=ErrorCode.NOT_FOUND,
            message="Tarefa não encontrada",
            validation_errors=[]
        )
    
    await db.delete(task)
    await db.commit()
    return task

async def get_challenge_task(
    db: AsyncSession,
    task_id: int
) -> Optional[ChallengeTask]:
    result = await db.execute(
        select(ChallengeTask)
        .options(
            joinedload(ChallengeTask.completed_tasks)
            .joinedload(CompletedChallengeTask.guest)
        )
        .where(ChallengeTask.id == task_id)
    )
    return result.unique().scalar_one_or_none()

# CompletedChallengeTask CRUD
async def complete_challenge_task(
    db: AsyncSession,
    complete_in: CompletedChallengeTaskCreate
) -> CompletedChallengeTask:
    # Criar a nova tarefa completada
    db_completed = CompletedChallengeTask(
        task_id=complete_in.task_id,
        photo_id=complete_in.photo_id,
        guest_id=complete_in.guest_id
    )

    db.add(db_completed)
    await db.commit()
    await db.refresh(db_completed)
    
    return db_completed

async def get_completed_challenge_task(
    db: AsyncSession,
    task_id: int,
    guest_id: int
) -> Optional[CompletedChallengeTask]:
    result = await db.execute(
        select(CompletedChallengeTask)
        .where(CompletedChallengeTask.task_id == task_id, CompletedChallengeTask.guest_id == guest_id)
    )
    return result.unique().scalar_one_or_none()

async def get_challenge_summary_by_guest(
    db: AsyncSession,
    guest_id: int,
    challenge_id: int
) -> Dict:
    stmt = (
        select(ChallengeTask)
        .options(
            joinedload(ChallengeTask.completed_tasks)
            .joinedload(CompletedChallengeTask.guest)
        )
        .where(ChallengeTask.challenge_id == challenge_id)
        .order_by(ChallengeTask.created_at)

    )
    result = await db.execute(stmt)
    result = result.unique().scalars().all()

    result_list = []

    task_map = {
        task.id: any(completed_task.guest_id == guest_id for completed_task in task.completed_tasks)
        for task in result
    }

    for task in result:
        result_list.append(ChallengeTaskResponseGuest(
            id=task.id,
            title=task.title,
            description=task.description,
            challenge_id=task.challenge_id,
            created_at=task.created_at,
            is_completed=task_map[task.id],
        ))
    return ChallengeSummaryGuestResponse(
        tasks=result_list
    )



async def get_challenge_summary(
    db: AsyncSession,
    challenge_id: int
) -> Dict:
    # Buscar o desafio com todas as tasks e completions
    challenge = await db.execute(
        select(PhotoChallenge)
        .options(
            joinedload(PhotoChallenge.tasks)
            .joinedload(ChallengeTask.completed_tasks)
            .joinedload(CompletedChallengeTask.guest)
        )
        .where(PhotoChallenge.id == challenge_id)
    )
    challenge = challenge.unique().scalar_one_or_none()
    
    if not challenge:
        return None
    
    total_tasks = len(challenge.tasks)
    tasks_with_completions = sum(1 for task in challenge.tasks if task.completed_tasks)
    pending_tasks = total_tasks - tasks_with_completions
    completion_percentage = (tasks_with_completions / total_tasks * 100) if total_tasks > 0 else 0
    
    # Contagem de participação por convidado
    guest_participation = defaultdict(int)
    
    # Preparar as tasks com informações de conclusão
    tasks = []
    for task in challenge.tasks:
        completed_info = []
        for completion in task.completed_tasks:
            guest_participation[completion.guest.name] += 1
            completed_info.append({
                "completed_at": completion.completed_at,
                "guest": {
                    "id": completion.guest.id,
                    "name": completion.guest.name
                },
                "photo_id": completion.photo_id
            })
        
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "challenge_id": task.challenge_id,
            "created_at": task.created_at,
            "is_completed": bool(task.completed_tasks),
            "completed_by": completed_info
        }
        tasks.append(task_dict)
    
    # Converter o defaultdict para lista de dicionários
    guests_participation = [
        {"guest_name": name, "tasks_completed": count}
        for name, count in guest_participation.items()
    ]
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": tasks_with_completions,
        "pending_tasks": pending_tasks,
        "completion_percentage": completion_percentage,
        "tasks": tasks,
        "guests_participation": guests_participation
    }
