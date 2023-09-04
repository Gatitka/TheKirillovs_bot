import sqlite3


class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?",
                                     (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?",
                                     (user_id,))
        return result.fetchone()[0]

    def add_record(self, user_id, category, value, comment):
        """Создаем запись о расходе"""
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
        #         "SELECT * FROM `records` WHERE `user_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`"
        #     )
        # if (within == 'month'):
        #     # за последний месяц
        #     result = self.cursor.execute(
        #         "SELECT * FROM 'records' WHERE 'user_id' = ? AND 'date' BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY 'date'"
        #     )
        return result.fetchall()[0]

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()

    # def add_user(self, user_id):
    #     """Добавляем юзера в базу"""
    #     self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)",
    #                         (user_id,))
    #     return self.conn.commit()
