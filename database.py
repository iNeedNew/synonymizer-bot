import sqlite3
from datetime import datetime


def connect_db():
    """Установить соединение с БД"""
    with sqlite3.connect('db_words.sqlite', check_same_thread=False) as con:
        con.row_factory = sqlite3.Row
        return con


class DataBase:
    """Класс с основными методами для работы с БД"""

    def __init__(self, db):

        self.__db = db
        self.__cur = db.cursor()

    def create_db(self):
        """Создание таблиц"""
        try:
            self.__cur.execute("""
                CREATE TABLE IF NOT EXISTS words(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word_name TEXT)"""
                               )

            self.__cur.execute("""    
                CREATE TABLE IF NOT EXISTS synonyms(
                word_id INTEGER,
                synonym_name TEXT)"""
                               )

            self.__cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id_user INTEGER,
                username TEXT,
                first_name TEXT,
                last_name TEXT
                )""")

            self.__cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions(
                user_id INTEGER,
                looking_word TEXT,
                request_time TEXT
                )""")


        except sqlite3.DataError as error:
            print('Error:', error)

    def get_id_word_of_db(self, word):
        """Взять ID слова в БД"""
        try:
            result = self.__cur.execute('SELECT id FROM words WHERE word_name=(?)', (word,)).fetchone()

            if result is None: return 0

            return result['id']

        except sqlite3.DataError as error:
            print('Error:', error)
            return 0

    def add_word_and_symbols_in_db(self, word, synonyms):
        """Добавить слово и его синонимы в БД"""
        try:
            self.__cur.execute('INSERT INTO words VALUES (NULL, ?)', (word,))
            word_id = self.get_id_word_of_db(word)
            self.__cur.executemany('INSERT INTO synonyms VALUES (?, ?)', ([(word_id, synonym) for synonym in synonyms]))
            self.__db.commit()
            return True
        except sqlite3.DataError as error:
            print('Error', error)
            return False

    def get_symbols_of_db(self, word):
        """Взять синонимы слова из БД"""
        try:
            word_id = self.get_id_word_of_db(word)
            result = self.__cur.execute('SELECT synonym_name FROM synonyms WHERE word_id=(?)', (word_id,)).fetchall()
            return list(map(lambda l: l['synonym_name'], result))

        except sqlite3.DataError as error:
            print('Error:', error)
            return []

    def add_user_in_db(self, telegram_id_user, username, first_name, last_name):
        try:
            self.__cur.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?)',
                               (telegram_id_user, username, first_name, last_name))
            self.__db.commit()

        except sqlite3.DataError as error:
            print('Error', error)

    def get_id_user_of_db(self, telegram_id_user):
        """Взять ID слова в БД"""
        try:
            result = self.__cur.execute('SELECT id FROM users WHERE telegram_id_user=(?)',
                                        (telegram_id_user,)).fetchone()

            if result is None: return 0

            return result[0]

        except sqlite3.DataError as error:
            print('Error:', error)
            return 0

    def add_session_in_db(self, telegram_id_user, word):
        try:
            time = datetime.utcnow()
            user_id = self.get_id_user_of_db(telegram_id_user)
            self.__cur.execute('INSERT INTO sessions VALUES (?, ?, ?)', (user_id, word, time))
            self.__db.commit()
        except sqlite3.DataError as error:
            print('Error', error)
