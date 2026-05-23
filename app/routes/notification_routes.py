from fastapi import APIRouter
from pydantic import BaseModel
from app.controllers.notification_controller import list_notifications, list_notifications_by_user, create_new_notification, mark_notification_seen, delete_existing_notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

class NotificationRequest(BaseModel):
    user_id: int
    sender_id: int
    message: str

@router.get("/")
def get_all():
    return list_notifications()

@router.get("/user/{user_id}")
def get_by_user(user_id: int):
    return list_notifications_by_user(user_id)

@router.post("/")
def create(data: NotificationRequest):
    return create_new_notification(data.user_id, data.sender_id, data.message)

@router.put("/{id}/seen")
def seen(id: int):
    return mark_notification_seen(id)

@router.delete("/{id}")
def delete(id: int):
    return delete_existing_notification(id)
