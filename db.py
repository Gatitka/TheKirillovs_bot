import sqlite3
import config
import math


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_db_tables(self):
        """Создаем таблицу пользователей."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                admin   INTEGER DEFAULT 0
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records(
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     REFERENCES users (id) ON DELETE SET NULL
                            NOT NULL,
                comment     TEXT,
                value       DECIMAL NOT NULL,
                date        DATETIME DEFAULT ( (DATETIME('now') ) )
                            NOT NULL,
                category    TEXT char(20) NOT NULL);
        ''')
        return self.conn.commit()

    def manage_user(self, action, user_id):
        """Добавление/удаление юзера"""
        if action == 'add':
            self.cursor.execute("INSERT INTO users (user_id) VALUES (?)",
                                (user_id,))
        elif action == 'del':
            self.cursor.execute(f"DELETE FROM users WHERE user_id={user_id}")
        return self.conn.commit()

    def manage_admin(self, action, user_id):
        """Добавление/удаление админа"""
        if action == 'add':
            self.cursor.execute("UPDATE users SET admin=1 WHERE user_id = ?",
                                (user_id,))
        elif action == 'del':
            self.cursor.execute("UPDATE users SET admin=0 WHERE user_id= ?",
                                (user_id))
        return self.conn.commit()

    def isAdmin(self, user_id):
        """Проверка активного пользователя, админи ли он по его user_id"""
        try:
            db_result = self.cursor.execute(
                "SELECT admin FROM users WHERE user_id = ?",
                (user_id,)
            )
        except sqlite3.OperationalError:
            db_result_bool = False
        else:
            if not db_result:
                db_result_bool = bool(db_result.fetchall()[0][0])
            else:
                db_result_bool = False
        return (user_id == int(config.ADMIN_ID)) + db_result_bool

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        try:
            result = self.cursor.execute(
                "SELECT id FROM users WHERE user_id = ?",
                (user_id,)
            )
        except sqlite3.OperationalError:
            db_result_bool = False,
            no_tables = True
        else:
            db_result_bool = bool(len(result.fetchall()))
            no_tables = False
        return db_result_bool, no_tables

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?",
                                     (user_id,))
        return result.fetchone()[0]

    def add_record(self, user_id, category, value, comment):
        """Создаем запись о расходе"""
        value = round(value, 2)
        self.cursor.execute(
            "INSERT INTO `records` "
            + "(`user_id`, `value`, `comment`, `category`) "
            + "VALUES(?, ?, ?, ?)",
            (self.get_user_id(user_id),
             value,
             comment,
             category)
        )
        return self.conn.commit()

    def get_records(self):
        """Получаем историю операций за последний период"""

        result = self.cursor.execute(
            "SELECT SUM(`value`) "
            + "FROM `records` "
            + "WHERE `date` BETWEEN datetime('now', 'start of month') "
            + "AND datetime('now', 'localtime')"
        )

        # if (within == 'day'):
        #     # за последний день
        #     result = self.cursor.execute(
        #         "SELECT * FROM `records`
        #          WHERE `user_id` = ? AND `date`
        #              BETWEEN datetime('now', 'start of day')
        #              AND datetime('now', 'localtime')
        #          ORDER BY `date`"
        #     )
        # if (within == 'month'):
        #     # за последний месяц
        #     result = self.cursor.execute(
        #         "SELECT * FROM 'records'
        #          WHERE 'user_id' = ? AND 'date'
        #              BETWEEN datetime('now', 'start of month')
        #              AND datetime('now', 'localtime')
        #     ORDER BY 'date'"
        #     )
        value = result.fetchall()[0][0]
        if value is None:
            value = 0
        return round(value, 2)

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
