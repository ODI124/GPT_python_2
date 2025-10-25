"""
Database helper with optional MySQL backend and SQLite fallback.

Behavior:
- If `mysql-connector-python` is installed and connection to MySQL succeeds, use MySQL.
- Otherwise, use a local SQLite database file `emails_local.db` in the same folder.

Exposes: init_db, add_email, get_all_emails, get_pending_emails,
         update_status, update_email, delete_email
"""

import sqlite3
from pathlib import Path
import traceback

# Try to import mysql connector; keep it optional
try:
    import mysql.connector as mysql  # type: ignore
    from mysql.connector import errorcode  # type: ignore
except Exception:
    mysql = None
    errorcode = None

# MySQL configuration (change if needed)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'python',
    'user': 'python',
    'password': '123456',
    'charset': 'utf8mb4'
}

# SQLite fallback path
SQLITE_PATH = Path(__file__).parent / 'emails_local.db'

# runtime flag
USE_SQLITE = False


def _mysql_connect():
    if mysql is None:
        return None
    try:
        conn = mysql.connect(**DB_CONFIG)
        return conn
    except Exception:
        return None


def _choose_backend():
    global USE_SQLITE
    if mysql is None:
        USE_SQLITE = True
        return
    conn = _mysql_connect()
    if conn is None:
        USE_SQLITE = True
    else:
        try:
            conn.close()
        except Exception:
            pass
        USE_SQLITE = False


_choose_backend()


def init_db():
    """Create email table in the chosen backend."""
    if USE_SQLITE:
        SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(SQLITE_PATH)) as conn:
            cur = conn.cursor()
            cur.execute('''
            CREATE TABLE IF NOT EXISTS email (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient TEXT NOT NULL,
                subject TEXT,
                content TEXT,
                status TEXT DEFAULT '전송전'
            );
            ''')
            conn.commit()
    else:
        try:
            conn = mysql.connect(**DB_CONFIG)
        except Exception:
            # try to create database via admin connection
            try:
                cfg = DB_CONFIG.copy()
                cfg.pop('database', None)
                admin_conn = mysql.connect(**cfg)
                cur = admin_conn.cursor()
                cur.execute("CREATE DATABASE IF NOT EXISTS `{}` DEFAULT CHARACTER SET utf8mb4".format(DB_CONFIG['database']))
                cur.close()
                admin_conn.close()
                conn = mysql.connect(**DB_CONFIG)
            except Exception:
                # fallback to sqlite if mysql can't be initialized
                traceback.print_exc()
                global USE_SQLITE
                USE_SQLITE = True
                return init_db()

        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS email (
            id INT AUTO_INCREMENT PRIMARY KEY,
            recipient VARCHAR(255) NOT NULL,
            subject VARCHAR(255),
            content TEXT,
            status VARCHAR(20) DEFAULT '전송전'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        ''')
        conn.commit()
        cur.close()
        conn.close()


def add_email(recipient, subject, content, status='전송전'):
    if USE_SQLITE:
        with sqlite3.connect(str(SQLITE_PATH)) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO email (recipient, subject, content, status) VALUES (?, ?, ?, ?)',
                        (recipient, subject, content, status))
            conn.commit()
            return cur.lastrowid
    else:
        conn = mysql.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('INSERT INTO email (recipient, subject, content, status) VALUES (%s, %s, %s, %s)',
                    (recipient, subject, content, status))
        conn.commit()
        last = cur.lastrowid
        cur.close()
        conn.close()
        return last


def get_all_emails():
    if USE_SQLITE:
        with sqlite3.connect(str(SQLITE_PATH)) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM email ORDER BY id')
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
    else:
        conn = mysql.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM email ORDER BY id')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows


def get_pending_emails():
    if USE_SQLITE:
        with sqlite3.connect(str(SQLITE_PATH)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM email WHERE status != '완료' ORDER BY id")
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
    else:
        conn = mysql.connect(**DB_CONFIG)
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM email WHERE status != '완료' ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows


def update_status(email_id, status):
    if USE_SQLITE:
        with sqlite3.connect(str(SQLITE_PATH)) as conn:
            cur = conn.cursor()
            cur.execute('UPDATE email SET status=? WHERE id=?', (status, email_id))
            conn.commit()
    else:
        conn = mysql.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('UPDATE email SET status=%s WHERE id=%s', (status, email_id))
        conn.commit()
        cur.close()
        conn.close()


def update_email(email_id, recipient, subject, content):
    if USE_SQLITE:
        with sqlite3.connect(str(SQLITE_PATH)) as conn:
            cur = conn.cursor()
            cur.execute('UPDATE email SET recipient=?, subject=?, content=? WHERE id=?',
                        (recipient, subject, content, email_id))
            conn.commit()
    else:
        conn = mysql.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('UPDATE email SET recipient=%s, subject=%s, content=%s WHERE id=%s',
                    (recipient, subject, content, email_id))
        conn.commit()
        cur.close()
        conn.close()


def delete_email(email_id):
    if USE_SQLITE:
        with sqlite3.connect(str(SQLITE_PATH)) as conn:
            cur = conn.cursor()
            cur.execute('DELETE FROM email WHERE id=?', (email_id,))
            conn.commit()
    else:
        conn = mysql.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute('DELETE FROM email WHERE id=%s', (email_id,))
        conn.commit()
        cur.close()
        conn.close()
