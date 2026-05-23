from fastapi import APIRouter
from pydantic import BaseModel
from app.config.db_config import get_connection

router = APIRouter(prefix="/messages", tags=["Messages"])

class Message(BaseModel):
    sender_id: int
    receiver_id: int
    message: str

@router.post("/")
def send_message(data: Message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)",
        (data.sender_id, data.receiver_id, data.message)
    )
    conn.commit()
    conn.close()
    return {"ok": True}

@router.get("/{user1_id}/{user2_id}")
def get_messages(user1_id: int, user2_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, sender_id, receiver_id, message, created_at
        FROM messages
        WHERE (sender_id = %s AND receiver_id = %s)
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY created_at ASC
    """, (user1_id, user2_id, user2_id, user1_id))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "sender_id": r[1], "receiver_id": r[2], "message": r[3], "created_at": str(r[4])} for r in rows]

@router.get("/unread/{user_id}")
def get_unread(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages WHERE receiver_id = %s AND seen = 0", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return {"count": count}
