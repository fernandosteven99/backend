import os
import psycopg2

def get_connection():
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_1ugjFDsEAW0k@ep-rough-resonance-ambvbrlf-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )
    return psycopg2.connect(db_url)