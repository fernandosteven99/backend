from fastapi import APIRouter
from pydantic import BaseModel
from app.config.db_config import get_connection

router = APIRouter(prefix="/messages", tags=["Messages"])

class MessageRequest(BaseModel):
    sender_id: int
    receiver_id: int
    message: str

@router.get("/unread/{user_id}")
def get_unread(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages WHERE receiver_id = %s AND seen = FALSE", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return {"count": count}

@router.get("/{user_id}/{other_id}")
def get_conversation(user_id: int, other_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, sender_id, receiver_id, message, seen, created_at
        FROM messages
        WHERE (sender_id = %s AND receiver_id = %s)
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY created_at ASC
    """, (user_id, other_id, other_id, user_id))
    data = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "sender_id": r[1], "receiver_id": r[2], "message": r[3], "seen": r[4], "created_at": str(r[5])} for r in data]

@router.post("")
def send_message(data: MessageRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message, seen)
        VALUES (%s, %s, %s, FALSE)
    """, (data.sender_id, data.receiver_id, data.message))
    conn.commit()
    conn.close()
    return {"message": "Mensaje enviado"}

@router.put("/{message_id}/seen")
def mark_seen(message_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE messages SET seen = TRUE WHERE id = %s", (message_id,))
    conn.commit()
    conn.close()
    return {"message": "Mensaje leído"}
