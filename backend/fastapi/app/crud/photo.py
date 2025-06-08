from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.photo import Photo, PhotoAlbum
from app.schemas.photo import PhotoCreate, PhotoUpdate, PhotoAlbumCreate, PhotoAlbumUpdate
from app.services.s3 import s3_service
from app.crud import guest as guest_crud

# CRUD para Photo
async def create_photo(db: AsyncSession, photo_in: PhotoCreate) -> Photo:
    # Gera a chave do arquivo no S3
    s3_key = s3_service.generate_file_key_user(
        user_id=photo_in.user_id,
        filename=photo_in.filename
    )
    
    # Gera URL pré-assinada para upload
    presigned_post = s3_service.generate_presigned_post(s3_key)

    #realiza o upload do arquivo para o S3
    is_uploaded = s3_service.upload_file(s3_key, photo_in.file)
    if not is_uploaded and False: #TODO: Remover o False para ativar o upload do arquivo para o S3
        raise HTTPException(status_code=500, detail="Erro ao fazer upload do arquivo para o S3")
    
    db_photo = Photo(
        filename=photo_in.filename,
        s3_key=s3_key,
        user_id=photo_in.user_id,
    )
    db.add(db_photo)
    await db.commit()
    await db.refresh(db_photo)
    return db_photo

async def get_photo(db: AsyncSession, photo_id: int) -> Optional[Photo]:
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    return result.unique().scalar_one_or_none()

async def get_user_photos(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[Photo]:
    result = await db.execute(
        select(Photo)
        .where(Photo.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_photo(db: AsyncSession, photo_id: int, photo_in: PhotoUpdate) -> Optional[Photo]:
    db_photo = await get_photo(db, photo_id)
    if not db_photo:
        return None
    
    for field, value in photo_in.model_dump(exclude_unset=True).items():
        setattr(db_photo, field, value)
    
    await db.commit()
    await db.refresh(db_photo)
    return db_photo

async def delete_photo(db: AsyncSession, photo_id: int) -> Optional[Photo]:
    db_photo = await get_photo(db, photo_id)
    if not db_photo:
        return None
    
    # Remove a foto do S3 antes de deletar do banco
    if db_photo.s3_key:
        s3_service.delete_file(db_photo.s3_key)
    
    await db.delete(db_photo)
    await db.commit()
    return db_photo

# CRUD para PhotoAlbum
async def create_photo_album(db: AsyncSession, album_in: PhotoAlbumCreate) -> PhotoAlbum:
    db_album = PhotoAlbum(
        name=album_in.name,
        description=album_in.description,
        user_id=album_in.user_id
    )
    db.add(db_album)
    await db.commit()
    await db.refresh(db_album)
    return db_album

async def get_photo_album(db: AsyncSession, album_id: int) -> Optional[PhotoAlbum]:
    result = await db.execute(select(PhotoAlbum).where(PhotoAlbum.id == album_id))
    return result.unique().scalar_one_or_none()

async def get_user_albums(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> List[PhotoAlbum]:
    result = await db.execute(
        select(PhotoAlbum)
        .where(PhotoAlbum.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_guest_albums(db: AsyncSession, guest_id: int) -> Optional[PhotoAlbum]:
    result = await db.execute(
        select(PhotoAlbum)
        .options(selectinload(PhotoAlbum.photos))
        .options(selectinload(PhotoAlbum.guest))
        .where(PhotoAlbum.guest_id == guest_id)
    )
    return result.unique().scalar_one_or_none()

async def get_guest_albums_or_create(db: AsyncSession, guest_id: int) -> Optional[PhotoAlbum]:
    album = await get_guest_albums(db=db, guest_id=guest_id)
    if not album:
        guest = await guest_crud.get_guest(db=db, guest_id=guest_id)
        album = await create_photo_album(
            db=db, 
            album_in=PhotoAlbumCreate(
                name=f"Álbum de fotos do convidado {guest.name}",
                description=f"Álbum de fotos do convidado {guest.name}",
                guest_id=guest_id,
                user_id=guest.user_id
            )
        )
    return album

async def update_photo_album(db: AsyncSession, album_id: int, album_in: PhotoAlbumUpdate) -> Optional[PhotoAlbum]:
    db_album = await get_photo_album(db, album_id)
    if not db_album:
        return None
    
    for field, value in album_in.model_dump(exclude_unset=True).items():
        setattr(db_album, field, value)
    
    await db.commit()
    await db.refresh(db_album)
    return db_album

async def delete_photo_album(db: AsyncSession, album_id: int) -> Optional[PhotoAlbum]:
    db_album = await get_photo_album(db, album_id)
    if not db_album:
        return None
    
    # Remove o vínculo das fotos com o álbum antes de deletá-lo
    for photo in db_album.photos:
        photo.photo_album_id = None
    
    await db.delete(db_album)
    await db.commit()
    return db_album

# Funções auxiliares para gerenciamento de fotos em álbuns
async def add_photo_to_album(db: AsyncSession, album_id: int, photo_id: int) -> Optional[PhotoAlbum]:
    """
    Adiciona uma foto a um álbum atualizando o photo_album_id da foto
    """
    db_album = await get_photo_album(db, album_id)
    if not db_album:
        return None
    
    db_photo = await get_photo(db, photo_id)
    if not db_photo:
        return None
    
    db_photo.photo_album_id = album_id
    await db.commit()
    await db.refresh(db_album)
    return db_album

async def remove_photo_from_album(db: AsyncSession, album_id: int, photo_id: int) -> Optional[PhotoAlbum]:
    """
    Remove uma foto de um álbum definindo o photo_album_id como None
    """
    db_album = await get_photo_album(db, album_id)
    if not db_album:
        return None
    
    db_photo = await get_photo(db, photo_id)
    if not db_photo or db_photo.photo_album_id != album_id:
        return None
    
    db_photo.photo_album_id = None
    await db.commit()
    await db.refresh(db_album)
    return db_album

async def get_album_by_photo_id(db: AsyncSession, photo_id: int) -> Optional[PhotoAlbum]:
    """
    Recupera o álbum ao qual uma foto pertence
    """
    result = await db.execute(select(PhotoAlbum).join(PhotoAlbum.photos).where(Photo.id == photo_id))
    return result.scalar_one_or_none()