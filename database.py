import sqlite3

DB_NAME = 'videos.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            file_id TEXT NOT NULL,
            channel_post_link TEXT UNIQUE NOT NULL,
            description TEXT,
            download_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Database created successfully!")

def add_video(title, file_id, channel_post_link, description=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO videos (title, file_id, channel_post_link, description)
            VALUES (?, ?, ?, ?)
        ''', (title, file_id, channel_post_link, description))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_video_by_link(link):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT file_id, title, description FROM videos WHERE channel_post_link = ?', (link,))
    result = c.fetchone()
    conn.close()
    return result

def increment_download_count(link):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE videos SET download_count = download_count + 1 WHERE channel_post_link = ?', (link,))
    conn.commit()
    conn.close()

def get_all_videos():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, title, channel_post_link, download_count FROM videos')
    results = c.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_db()
