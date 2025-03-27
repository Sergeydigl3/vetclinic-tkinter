# database_module.py
import sqlite3
import datetime # Потребуется для добавления комментария с текущей датой
import base64 # Для кодирования/декодирования изображения

class DatabaseManager:
    def __init__(self, db_name='vet_clinic.db'):
        self.conn = sqlite3.connect(db_name)
        # Важно: Установить row_factory для удобного доступа к данным по именам колонок
        # self.conn.row_factory = sqlite3.Row # Раскомментируйте, если хотите использовать доступ как к словарю
        self.cursor = self.conn.cursor()
        # Включаем поддержку внешних ключей ПЕРЕД созданием таблиц или другими операциями
        self.cursor.execute("PRAGMA foreign_keys = ON;") # <-- Убедитесь, что это здесь
        self.create_tables()
        self._check_and_add_image_column() # Проверка и добавление колонки для изображения

    def _check_and_add_image_column(self):
        """Проверяет наличие колонки image_base64 в таблице animals и добавляет ее, если нет."""
        try:
            self.cursor.execute("PRAGMA table_info(animals)")
            columns = [info[1] for info in self.cursor.fetchall()]
            if 'image_base64' not in columns:
                print("Adding 'image_base64' column to 'animals' table...")
                self.cursor.execute('ALTER TABLE animals ADD COLUMN image_base64 TEXT')
                self.conn.commit()
                print("'image_base64' column added.")
        except sqlite3.Error as e:
            print(f"Ошибка при проверке/добавлении колонки image_base64: {e}")
            # Не прерываем работу, возможно таблица еще не создана (хотя create_tables вызывается раньше)

    def create_tables(self):
        # Создание таблиц базы данных
        # PRAGMA foreign_keys = ON; уже выполнен в __init__

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )
        ''')

        # Обновлено: Добавлена колонка image_base64
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS animals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                type TEXT,
                breed TEXT,
                age INTEGER,
                image_base64 TEXT, -- <<< НОВАЯ КОЛОНКА
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER,
                comment TEXT NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(animal_id) REFERENCES animals(id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()

    # ... (user methods remain the same) ...
    def add_user(self, name, phone, email):
        try:
            self.cursor.execute(
                'INSERT INTO users (name, phone, email) VALUES (?, ?, ?)',
                (name, phone, email)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Ошибка добавления пользователя: {e}")
            self.conn.rollback() # Откатить транзакцию при ошибке
            raise # Передать исключение дальше

    def get_users(self):
        self.cursor.execute('SELECT id, name, phone, email FROM users ORDER BY name') # Добавил сортировку
        return self.cursor.fetchall()

    def delete_user(self, user_id):
        try:
            self.cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка удаления пользователя: {e}") # Ошибка все еще может возникнуть по другим причинам
            self.conn.rollback()
            raise # Передаем исключение выше (в VetClinicApp)

    def update_user(self, user_id, name, phone, email):
        """Обновляет данные пользователя в базе данных"""
        try:
            self.cursor.execute(
                'UPDATE users SET name=?, phone=?, email=? WHERE id=?',
                (name, phone, email, user_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка обновления пользователя: {e}")
            self.conn.rollback()
            raise # Передать исключение дальше

    # --- Animal Methods Updated ---

    # Обновлено: Добавлен параметр image_base64
    def add_animal(self, user_id, name, type_animal, breed, age, image_base64=None):
        """Добавляет новое животное, включая изображение."""
        try:
            self.cursor.execute(
                'INSERT INTO animals (user_id, name, type, breed, age, image_base64) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, name, type_animal, breed, age, image_base64)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Ошибка добавления животного: {e}")
            self.conn.rollback()
            raise

    # Обновлено: Выбирается колонка image_base64
    def get_animals_by_user(self, user_id):
        """Получает список животных для пользователя, включая данные изображения."""
        self.cursor.execute(
            'SELECT id, user_id, name, type, breed, age, image_base64 FROM animals WHERE user_id = ? ORDER BY name',
            (user_id,)
        )
        return self.cursor.fetchall()

    # Обновлено: Добавлен параметр image_base64
    def update_animal(self, animal_id, name, type_animal, breed, age, image_base64=None):
        """Обновляет данные животного, включая изображение."""
        try:
            self.cursor.execute(
                'UPDATE animals SET name=?, type=?, breed=?, age=?, image_base64=? WHERE id=?',
                (name, type_animal, breed, age, image_base64, animal_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка обновления животного: {e}")
            self.conn.rollback()
            raise

    def delete_animal(self, animal_id):
        """Удаляет животное и связанные с ним комментарии (через ON DELETE CASCADE)."""
        try:
            self.cursor.execute('DELETE FROM animals WHERE id = ?', (animal_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка удаления животного: {e}")
            self.conn.rollback()
            raise

    # --- Comment Methods (remain the same) ---
    def add_comment(self, animal_id, comment_text):
        try:
            self.cursor.execute(
                'INSERT INTO comments (animal_id, comment) VALUES (?, ?)',
                (animal_id, comment_text)
            )
            self.conn.commit()
            return self.cursor.lastrowid # Возвращаем ID добавленного комментария
        except sqlite3.Error as e:
            print(f"Ошибка добавления комментария: {e}")
            self.conn.rollback()
            raise

    def get_comments_by_animal(self, animal_id):
        self.cursor.execute('SELECT id, animal_id, comment, date FROM comments WHERE animal_id = ? ORDER BY date DESC', (animal_id,))
        return self.cursor.fetchall()

    def delete_comment(self, comment_id):
        """Удаляет комментарий по его ID."""
        try:
            self.cursor.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка удаления комментария: {e}")
            self.conn.rollback()
            raise

    def update_comment(self, comment_id, new_text):
        """Обновляет текст комментария в базе данных"""
        try:
            self.cursor.execute(
                'UPDATE comments SET comment=? WHERE id=?',
                (new_text, comment_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка обновления комментария: {e}")
            self.conn.rollback()
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.") # Сообщение для отладки