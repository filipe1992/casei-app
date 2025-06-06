from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import photo as photo_crud, guest as guest_crud
from app.schemas.photo import (
    Photo, PhotoCreate, PhotoResponse, PhotoUpdate,
    PhotoAlbum, PhotoAlbumCreate, PhotoAlbumUpdate, PhotoAlbumResponse
)
from app.models.user import User
from app.services.s3 import s3_service
from app.db.session import get_db
from app.auth.auth import get_current_user

router = APIRouter()

# Rotas para Photos
@router.post("/photos/", response_model=PhotoResponse)
async def create_photo(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Upload de foto pelo usuário
    """
    photo_in = PhotoCreate(
        filename=file.filename,
        user_id=current_user.id,
        file=file
    )

    photo = await photo_crud.create_photo(db=db, photo_in=photo_in)

    return PhotoResponse(
        id=photo.id,
        filename=photo.filename,
        s3_key=photo.s3_key,
        user_id=photo.user_id,
        upload_date=photo.upload_date,
        photo_album_id=photo.photo_album_id,
        url=s3_service.generate_presigned_url(photo.s3_key)
    )

# upload de foto de um convidado
@router.post("/guests/{guest_hash_link}/albums/{album_id}/photos/", response_model=PhotoResponse)
async def create_guest_photo(
    guest_hash_link: str,
    album_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Upload de foto de um convidado
    """
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash_link)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.user_id != guest.user_id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    contents = await file.read()
    photo_in = PhotoCreate(
        filename=file.filename,
        user_id=guest.user_id,
        file=contents
    )
    
    photo = await photo_crud.create_photo(db=db, photo_in=photo_in)
    
    return PhotoResponse(
        id=photo.id,
        filename=photo.filename,
        s3_key=photo.s3_key,
        user_id=photo.user_id,
        upload_date=photo.upload_date,
        photo_album_id=photo.photo_album_id,
        url=s3_service.generate_presigned_url(photo.s3_key)
    )

@router.get("/photos/", response_model=List[PhotoResponse])
async def read_user_photos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar todas as fotos do usuário
    """
    photos = await photo_crud.get_user_photos(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    return [
        PhotoResponse(
            **photo.__dict__,
            url=s3_service.generate_presigned_url(photo.s3_key)
        )
        for photo in photos
    ]

@router.get("/photos/{photo_id}", response_model=PhotoResponse)
async def read_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar uma foto específica
    """
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return PhotoResponse(
        id=photo.id,
        filename=photo.filename,
        s3_key=photo.s3_key,
        user_id=photo.user_id,
        upload_date=photo.upload_date,
        photo_album_id=photo.photo_album_id,
        url=s3_service.generate_presigned_url(photo.s3_key)
    )

# recupera foto de um álbum pelo hash link
@router.get("/guests/{guest_hash_link}/albums/{album_id}/photos/{photo_id}", response_model=PhotoResponse)
async def read_guest_photo(
    guest_hash_link: str,
    album_id: int,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Recuperar uma foto específica de um álbum de um convidado
    """
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash_link)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.user_id != guest.user_id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != guest.user_id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return PhotoResponse(
        id=photo.id,
        filename=photo.filename,
        s3_key=photo.s3_key,
        user_id=photo.user_id,
        upload_date=photo.upload_date,
        photo_album_id=photo.photo_album_id,
        url=s3_service.generate_presigned_url(photo.s3_key)
    )

@router.put("/photos/{photo_id}", response_model=Photo)
async def update_photo(
    photo_id: int,
    photo_in: PhotoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar uma foto
    """
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return await photo_crud.update_photo(db=db, photo_id=photo_id, photo_in=photo_in)

@router.delete("/photos/{photo_id}", response_model=Photo)
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar uma foto
    """
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return await photo_crud.delete_photo(db=db, photo_id=photo_id)

# Rotas para PhotoAlbum
@router.post("/albums/", response_model=PhotoAlbumResponse)
async def create_album(
    album_in: PhotoAlbumCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Criar um novo álbum
    """
    if album_in.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é permitido criar álbuns para outros usuários"
        )
    
    album = await photo_crud.create_photo_album(db=db, album_in=album_in)
    
    # Se o álbum for de um convidado, busca o nome do convidado
    guest_name = None
    if album.guest_id:
        guest = await guest_crud.get_guest(db=db, guest_id=album.guest_id)
        if guest:
            guest_name = guest.name
    
    return PhotoAlbumResponse(
        id=album.id,
        name=album.name,
        description=album.description,
        user_id=album.user_id,
        guest_id=album.guest_id,
        created_at=album.created_at,
        photos=album.photos,
        guest_name=guest_name
    )

@router.get("/albums/", response_model=List[PhotoAlbumResponse])
async def read_albums(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar todos os álbuns do usuário
    """
    albums = await photo_crud.get_user_albums(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    # Adiciona o nome do convidado para álbuns de convidados
    result = []
    for album in albums:
        guest_name = None
        if album.guest_id:
            guest = await guest_crud.get_guest(db=db, guest_id=album.guest_id)
            if guest:
                guest_name = guest.name
        
        result.append(PhotoAlbumResponse(
            id=album.id,
            name=album.name,
            description=album.description,
            user_id=album.user_id,
            guest_id=album.guest_id,
            created_at=album.created_at,
            photos=album.photos,
            guest_name=guest_name
        ))
    
    return result

@router.get("/albums/{album_id}", response_model=PhotoAlbumResponse)
async def read_album(
    album_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Recuperar um álbum específico
    """
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    # Se o álbum for de um convidado, busca o nome do convidado
    guest_name = None
    if album.guest_id:
        guest = await guest_crud.get_guest(db=db, guest_id=album.guest_id)
        if guest:
            guest_name = guest.name
    
    return PhotoAlbumResponse(
        **album.__dict__,
        guest_name=guest_name
    )

@router.put("/albums/{album_id}", response_model=PhotoAlbumResponse)
async def update_album(
    album_id: int,
    album_in: PhotoAlbumUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Atualizar um álbum
    """
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    updated_album = await photo_crud.update_photo_album(db=db, album_id=album_id, album_in=album_in)
    
    # Se o álbum for de um convidado, busca o nome do convidado
    guest_name = None
    if updated_album.guest_id:
        guest = await guest_crud.get_guest(db=db, guest_id=updated_album.guest_id)
        if guest:
            guest_name = guest.name
    
    return PhotoAlbumResponse(
        **updated_album.__dict__,
        guest_name=guest_name
    )

@router.delete("/albums/{album_id}", response_model=PhotoAlbum)
async def delete_album(
    album_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Deletar um álbum
    """
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    return await photo_crud.delete_photo_album(db=db, album_id=album_id)

@router.post("/albums/{album_id}/photos/{photo_id}", response_model=PhotoAlbum)
async def add_photo_to_album(
    album_id: int,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Adicionar uma foto a um álbum
    """
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return await photo_crud.add_photo_to_album(db=db, album_id=album_id, photo_id=photo_id)

# adiciona foto a um álbum de um convidado
@router.post("/guests/{guest_hash_link}/albums/{album_id}/photos/{photo_id}", response_model=PhotoAlbum)
async def add_photo_to_guest_album(
    guest_hash_link: str,
    album_id: int,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Adicionar uma foto a um álbum de um convidado
    """
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash_link)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.guest_id != guest.id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != guest.user_id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return await photo_crud.add_photo_to_album(db=db, album_id=album_id, photo_id=photo_id)

@router.delete("/albums/{album_id}/photos/{photo_id}", response_model=PhotoAlbum)
async def remove_photo_from_album(
    album_id: int,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Remover uma foto de um álbum
    """
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return await photo_crud.remove_photo_from_album(db=db, album_id=album_id, photo_id=photo_id)

# remove foto de um álbum de um convidado
@router.delete("/guests/{guest_hash_link}/albums/{album_id}/photos/{photo_id}", response_model=PhotoAlbum)
async def remove_photo_from_guest_album(
    guest_hash_link: str,
    album_id: int,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Remover uma foto de um álbum de um convidado
    """
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash_link)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    album = await photo_crud.get_photo_album(db=db, album_id=album_id)
    if not album or album.guest_id != guest.id:
        raise HTTPException(status_code=404, detail="Álbum não encontrado")
    
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    if not photo or photo.user_id != guest.user_id:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    return await photo_crud.remove_photo_from_album(db=db, album_id=album_id, photo_id=photo_id)

@router.get("/photos/{photo_id}/album/{guest_hash_link}", response_model=PhotoAlbumResponse)
async def get_photo_album_info(
    photo_id: int,
    guest_hash_link: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Recuperar informações do álbum ao qual uma foto pertence
    """
    photo = await photo_crud.get_photo(db=db, photo_id=photo_id)
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash_link)
    if not photo or not guest:
        raise HTTPException(status_code=404, detail="Foto ou convidado não encontrado")
    
    if photo.user_id != guest.user_id:
        raise HTTPException(status_code=404, detail="Foto não pertence ao convidado")
    
    album = await photo_crud.get_album_by_photo_id(db=db, photo_id=photo_id)
    if not album:
        raise HTTPException(status_code=404, detail="Foto não pertence a nenhum álbum")
    
    # Se o álbum for de um convidado, busca o nome do convidado
    guest_name = None
    if album.guest_id:
        guest = await guest_crud.get_guest(db=db, guest_id=album.guest_id)
        if guest:
            guest_name = guest.name
    
    return PhotoAlbumResponse(
        **album.__dict__,
        guest_name=guest_name
    ) 

# recupera album de fotos de um convidado pelo hash link
@router.get("/guests/{guest_hash_link}/albums/", response_model=List[PhotoAlbumResponse])
async def read_guest_albums(
    guest_hash_link: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Recuperar todos os álbuns de fotos de um convidado específico pelo hash link
    """
    guest = await guest_crud.get_guest_by_hash(db=db, hash_link=guest_hash_link)
    if not guest:
        raise HTTPException(status_code=404, detail="Convidado não encontrado")
    
    albums = await photo_crud.get_guest_albums(db=db, guest_id=guest.id)
    
    return [
        PhotoAlbumResponse(
            **album.__dict__,
            guest_name=guest.name
        )
        for album in albums
    ]