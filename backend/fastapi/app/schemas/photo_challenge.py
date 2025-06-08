from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


# Schemas para ChallengeTask
class ChallengeTaskBase(BaseModel):
    title: str
    description: str

class ChallengeTaskCreate(ChallengeTaskBase):
    pass

class ChallengeTaskUpdate(ChallengeTaskBase):
    pass

# Schemas para PhotoChallenge
class PhotoChallengeBase(BaseModel):
    title: str

class PhotoChallengeCreate(PhotoChallengeBase):
    tasks: List[ChallengeTaskCreate] = []
    pass

class PhotoChallengeUpdate(PhotoChallengeBase):
    pass

# Schemas para CompletedChallengeTask
class CompletedChallengeTaskBase(BaseModel):
    task_id: int
    photo_id: int
    guest_id: int

class CompletedChallengeTaskCreate(CompletedChallengeTaskBase):
    pass

class CompletedChallengeTaskPhoto(BaseModel):
    id: int
    filename: str
    upload_date: datetime
    hash_id: str
    user_id: int
    guest_id: int

class GuestInfo(BaseModel):
    id: int
    name: str

class CompletedTaskInfo(BaseModel):
    completed_at: datetime
    guest: GuestInfo
    photo_id: int

    class Config:
        from_attributes = True

# Response Schemas
class ChallengeTaskResponse(ChallengeTaskBase):
    id: int
    challenge_id: int
    created_at: datetime
    completed_tasks: List[CompletedTaskInfo] = []

    class Config:
        from_attributes = True

# Response Schemas
class ChallengeTaskResponseGuest(ChallengeTaskBase):
    id: int
    challenge_id: int
    created_at: datetime
    is_completed: bool = False
    completed_tasks: List[CompletedTaskInfo] = []

    class Config:
        from_attributes = True

class PhotoChallengeResponse(PhotoChallengeBase):
    id: int
    created_at: datetime
    user_id: int
    tasks: List[ChallengeTaskResponse]

    class Config:
        from_attributes = True

class ChallengeSummaryResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_percentage: float
    tasks: List[ChallengeTaskResponse]
    guests_participation: List[dict] = []  # Lista com contagem de tarefas por convidado

class ChallengeSummaryGuestResponse(BaseModel):
    tasks: List[ChallengeTaskResponseGuest]