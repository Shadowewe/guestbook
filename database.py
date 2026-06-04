import sqlite3
from datetime import date

DATABASE = 'guestbook.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Таблица сообщений (уже есть)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')
    
    # ========== НОВАЯ ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ ==========
    # UNIQUE означает, что логины не могут повторяться
    # NOT NULL — поле обязательно для заполнения
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    # Добавляем администратора, если его ещё нет
    # INSERT OR IGNORE — если такой логин уже есть, не добавляем повторно
    # Пароль хранится как есть (в учебных целях, в реальных проектах пароли хэшируют!)
    conn.execute(
        'INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',
        ('admin', '123')
    )
    
    conn.commit()
    conn.close()

def get_all_messages():
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT * FROM messages ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return messages

def add_message(name, message):
    """
    Добавляет новое сообщение в базу данных.
    Дата создания проставляется автоматически (текущая дата).
    """
    # Получаем соединение с базой данных
    conn = get_db_connection()
    
    conn.execute(
        'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
        (name, message, date.today().strftime('%Y-%m-%d'))
    )
    conn.commit()
    conn.close()

def delete_message(message_id):
    """Удаляет сообщение из базы данных по его id."""
    conn = get_db_connection()
    conn.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

def delete_all():
    conn = get_db_connection()
    conn.execute('DELETE FROM messages')
    conn.commit()
    conn.close()

def get_message_count():
    """Возвращает общее количество сообщений."""
    conn = get_db_connection()
    cursor = conn.execute('SELECT COUNT(*) FROM messages')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def sort_newest():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM messages ORDER BY created_at DESC')
    conn.commit()

def sort_oldest():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM messages ORDER BY created_at ASC')
    conn.commit()

def check_user(username, password):
    """
    Проверяет, существует ли пользователь с таким логином и паролем.
    Возвращает True, если пользователь найден, иначе False.
    """
    conn = get_db_connection()
    # SELECT * FROM users — берём все поля
    # WHERE username = ? AND password = ? — ищем точное совпадение
    # ? — защита от SQL-инъекций
    user = conn.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()  # fetchone() — возвращает одну строку или None
    conn.close()
    
    # Если user не None, значит пользователь найден
    return user is not None

    # Сохраняем изменения
    conn.commit()
    
    # Закрываем соединение
    conn.close()