from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.crud import photo as photo_crud
from app.crud import guest as guest_crud
from app.schemas.photo import Photo, PhotoCreate, PhotoResponse
from app.models.user import User
from app.db.session import get_db
from app.auth.auth import get_current_user
from app.services.s3 import s3_service

router = APIRouter()

@router.post("/upload/{guest_hash}", response_model=PhotoResponse)
async def upload_photo(
    guest_hash: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> Any:
    """
    Upload de foto por um convidado usando seu hash único
    """
    # Busca o convidado pelo hash
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise HTTPException(
            status_code=404,
            detail="Convidado não encontrado"
        )

    photo, presigned_post = await photo_crud.create_photo(
        db=db,
        file=file,
        user_id=guest.user_id,
        guest_id=guest.id
    )


    return PhotoResponse(
            id=photo.id,
            filename=photo.filename,
            s3_key=photo.s3_key,
            upload_date=photo.upload_date,
            hash_id=photo.hash_id,
            user_id=photo.user_id,
            guest_id=photo.guest_id,
            guest_name= guest.name,
            url=presigned_post["url"]
        )

@router.get("/guest/{guest_hash}", response_model=List[PhotoResponse])
async def read_guest_photos(
    guest_hash: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Any:
    """
    Recuperar fotos de um convidado específico usando seu hash
    """
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash)
    if not guest:
        raise HTTPException(
            status_code=404,
            detail="Convidado não encontrado"
        )
    
    photos = await photo_crud.get_photos_by_guest(
        db=db,
        guest_id=guest.id,
        skip=skip,
        limit=limit
    )
    
    return [
        PhotoResponse(
            id=photo.id,
            filename=photo.filename,
            s3_key=photo.s3_key,
            upload_date=photo.upload_date,
            hash_id=photo.hash_id,
            user_id=photo.user_id,
            guest_id=photo.guest_id,
            guest_name=guest.name,
            url=s3_service.generate_presigned_url(photo.s3_key)
        )
        for photo in photos
    ]

@router.get("/user", response_model=List[PhotoResponse])
async def read_user_photos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar todas as fotos do usuário (dono do evento)
    """
    photos = await photo_crud.get_photos_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    return [
        PhotoResponse(
            id=photo.id,
            filename=photo.filename,
            s3_key=photo.s3_key,
            upload_date=photo.upload_date,
            hash_id=photo.hash_id,
            user_id=photo.user_id,
            guest_id=photo.guest_id,
            guest_name= (await guest_crud.get_guest(db=db, guest_id=photo.guest_id)).name,
            url=s3_service.generate_presigned_url(photo.s3_key)
        )
        for photo in photos
    ]

@router.get("/user/guest/{guest_id}", response_model=List[PhotoResponse])
async def read_guest_photos_by_id(
    guest_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar fotos de um convidado específico (apenas para o dono do evento)
    """
    guest = await guest_crud.get_guest(db=db, guest_id=guest_id)
    if not guest or guest.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="Convidado não encontrado"
        )
    
    photos = await photo_crud.get_photos_by_guest(
        db=db,
        guest_id=guest_id,
        skip=skip,
        limit=limit
    )
    
    return [
        PhotoResponse(
            id=photo.id,
            filename=photo.filename,
            s3_key=photo.s3_key,
            upload_date=photo.upload_date,
            hash_id=photo.hash_id,
            user_id=photo.user_id,
            guest_id=photo.guest_id,
            guest_name=guest.name,
            url=s3_service.generate_presigned_url(photo.s3_key)
        )
        for photo in photos
    ]

@router.delete("/{photo_id}", response_model=Photo)
async def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar uma foto (apenas usuário dono do evento pode deletar)
    """
    photo = await photo_crud.delete_photo(
        db=db,
        photo_id=photo_id,
        user_id=current_user.id
    )
    
    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Foto não encontrada"
        )
    
    return photo 