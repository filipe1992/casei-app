from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.models.photo import Photo
from app.schemas.photo import PhotoCreate
from app.services.s3 import s3_service

async def create_photo(
    db: AsyncSession,
    file: UploadFile,
    user_id: int,
    guest_id: int
) -> Photo:
    hash_id = str(uuid.uuid4())

    # Gera a chave do arquivo no S3
    s3_key = s3_service.generate_file_key(
        user_id=user_id,
        guest_id=guest_id,
        filename=file.filename
    )
    
    # Gera URL pré-assinada para upload
    presigned_post = s3_service.generate_presigned_post(s3_key)

    photo_in = PhotoCreate(
        filename=file.filename,
        s3_key=s3_key
    )

    #realiza o upload do arquivo para o S3
    is_uploaded = s3_service.upload_file(s3_key, file)
    if not is_uploaded and False: #TODO: Remover o False para ativar o upload do arquivo para o S3
        raise HTTPException(status_code=500, detail="Erro ao fazer upload do arquivo para o S3")
    
    db_photo = Photo(
        filename=photo_in.filename,
        s3_key=photo_in.s3_key,
        hash_id=hash_id,
        user_id=user_id,
        guest_id=guest_id,
    )
    
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    return db_photo, presigned_post

async def get_photo(db: AsyncSession, photo_id: int) -> Optional[Photo]:
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    return result.scalar_one_or_none()

async def get_photos_by_user(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Photo]:
    result = await db.execute(
        select(Photo)
        .where(Photo.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_photos_by_guest(
    db: AsyncSession,
    guest_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Photo]:
    result = await db.execute(
        select(Photo)
        .where(Photo.guest_id == guest_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def delete_photo(
    db: AsyncSession,
    photo_id: int,
    user_id: int
) -> Optional[Photo]:
    result = await db.execute(
        select(Photo).where(
            Photo.id == photo_id,
            Photo.user_id == user_id
        )
    )
    photo = result.scalar_one_or_none()
    
    if photo:
        # Deletar arquivo do S3
        s3_service.delete_file(photo.s3_key)
        
        # Deletar registro do banco de dados
        await db.delete(photo)
        await db.commit()
    
    return photo 