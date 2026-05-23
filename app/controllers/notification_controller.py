from app.models.notification_model import get_notifications, get_notifications_by_user, create_notification, mark_as_seen, delete_notification

def list_notifications():
    return get_notifications()

def list_notifications_by_user(user_id: int):
    return get_notifications_by_user(user_id)

def create_new_notification(user_id: int, sender_id: int, message: str):
    create_notification(user_id, sender_id, message)
    return {"message": "Notificación enviada"}

def mark_notification_seen(notification_id: int):
    mark_as_seen(notification_id)
    return {"message": "Notificación marcada como leída"}

def delete_existing_notification(id: int):
    delete_notification(id)
    return {"message": "Notificación eliminada"}
