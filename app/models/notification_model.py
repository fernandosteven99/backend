from app.config.db_config import get_connection

def get_notifications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT n.id, n.user_id, n.sender_id, n.message, n.seen, n.created_at,
               u.nombre as recipient, s.nombre as sender
        FROM notifications n
        JOIN users u ON n.user_id = u.id
        LEFT JOIN users s ON n.sender_id = s.id
        ORDER BY n.created_at DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "user_id": r[1], "sender_id": r[2], "message": r[3], "seen": r[4], "created_at": str(r[5]), "recipient": r[6], "sender": r[7]} for r in data]

def get_notifications_by_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT n.id, n.user_id, n.sender_id, n.message, n.seen, n.created_at,
               s.nombre as sender
        FROM notifications n
        LEFT JOIN users s ON n.sender_id = s.id
        WHERE n.user_id = %s
        ORDER BY n.created_at DESC
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "user_id": r[1], "sender_id": r[2], "message": r[3], "seen": r[4], "created_at": str(r[5]), "sender": r[6]} for r in data]

def create_notification(user_id: int, sender_id: int, message: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (user_id, sender_id, message, seen) VALUES (%s, %s, %s, FALSE)",
        (user_id, sender_id, message)
    )
    conn.commit()
    conn.close()

def mark_as_seen(notification_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET seen = TRUE WHERE id = %s", (notification_id,))
    conn.commit()
    conn.close()

def delete_notification(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notifications WHERE id = %s", (id,))
    conn.commit()
    conn.close()
