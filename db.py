import sqlite3

import config


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

    def is_admin(self, user_id):
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
        value = result.fetchall()[0][0]
        if value is None:
            value = 0
        return round(value, 2)

    def get_monthly_report(self, monthly_expenses):
        result = self.cursor.execute(
            "SELECT category, SUM(`value`) AS SUM_VALUE "
            + "FROM `records` "
            + "WHERE `date` "
            + "BETWEEN datetime('now', 'start of month') "
            + "AND datetime('now', 'localtime') "
            + "GROUP BY category "
            + "ORDER BY SUM_VALUE DESC"
        )
        result = result.fetchall()
        total_value = 0
        for i in result:
            total_value += i[1]
        total_value = round(total_value, 2)
        message = 'Саммери затрат за последний месяц:\n'
        for i in result:
            perc = int(i[1] / total_value * 100)
            message += f' - {i[0]} {i[1]}€ {perc}%\n'
        fact_vs_budget = int(total_value / monthly_expenses * 100)
        if fact_vs_budget > 100:
            message += (f'\nИтого потрачено {total_value}€\n'
                        + f'Перерасход бюджета {fact_vs_budget - 100}%\n\n'
                        + 'НУ ЧТО Ж... иди ебашь')
        else:
            message += (f'\nИтого потрачено {total_value}€\n'
                        + f'Экономия бюджета {100 - fact_vs_budget}%\n\n'
                        + 'МОЛОДЦЫ!!!'
                        )
        return message

    def get_today_report(self, monthly_expenses):
        # за последний день
        result = self.cursor.execute(
            "SELECT strftime('%d.%m %H:%M', date) AS formatted_date, "
            + "category, value, comment FROM 'records' "
            + "WHERE `date` "
            + "BETWEEN datetime('now', 'start of day') "
            + "AND datetime('now', 'localtime') "
            + "ORDER BY `date`"
        )
        result = result.fetchall()
        if result:
            message = 'Записи за сегодня:\n'
            for i in result:
                message += f'-> {i[0]} {i[1]} {i[2]}€ {i[3]}\n'
        else:
            message = 'Записей сегодня нет.'
        return message

    def get_detail_month_report(self, monthly_expenses):
        # за последний месяц
        result = self.cursor.execute(
            "SELECT strftime('%d.%m %H:%M', date) AS formatted_date, "
            + "category, value, comment FROM 'records' "
            + "WHERE `date` "
            + "BETWEEN datetime('now', 'start of month') "
            + "AND datetime('now', 'localtime') "
            + "ORDER BY 'date'"
        )
        result = result.fetchall()
        if result:
            message = 'Записи этого месяца:\n'
            for i in result:
                message += f'-> {i[0]} {i[1]} {i[2]}€ {i[3]}\n'
        else:
            message = 'Записей в этом месяце нет.'
        return message

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
