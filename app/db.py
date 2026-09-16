import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from app.config import DATABASE_PATH
Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
def conn():
    c=sqlite3.connect(DATABASE_PATH); c.row_factory=sqlite3.Row; return c
def init_db():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,username TEXT,first_name TEXT,created_at TEXT NOT NULL,last_seen TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT,channel_id TEXT NOT NULL,message_id INTEGER NOT NULL,text TEXT DEFAULT '',media_type TEXT DEFAULT '',file_id TEXT DEFAULT '',caption TEXT DEFAULT '',created_at TEXT NOT NULL,UNIQUE(channel_id,message_id))""")
def upsert_user(user_id,username,first_name):
    now=datetime.now(timezone.utc).isoformat()
    with conn() as c:
        c.execute("""INSERT INTO users(user_id,username,first_name,created_at,last_seen) VALUES(?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET username=excluded.username,first_name=excluded.first_name,last_seen=excluded.last_seen""",(user_id,username or '',first_name or '',now,now))
def add_post(channel_id,message_id,text='',media_type='',file_id='',caption=''):
    now=datetime.now(timezone.utc).isoformat()
    with conn() as c:
        c.execute("INSERT OR IGNORE INTO posts(channel_id,message_id,text,media_type,file_id,caption,created_at) VALUES(?,?,?,?,?,?,?)",(str(channel_id),message_id,text or '',media_type or '',file_id or '',caption or '',now))
def get_posts(limit=50):
    with conn() as c:return [dict(r) for r in c.execute('SELECT * FROM posts ORDER BY id DESC LIMIT ?',(limit,)).fetchall()]
def get_post(post_id):
    with conn() as c:
        r=c.execute('SELECT * FROM posts WHERE id=?',(post_id,)).fetchone(); return dict(r) if r else None
def user_count():
    with conn() as c:return c.execute('SELECT COUNT(*) n FROM users').fetchone()['n']
