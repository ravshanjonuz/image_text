import sqlite3


def logger(statement):
    if "BEGIN" in str(statement) or "COMMIT" in str(statement):
        return
    print("****** Executing => {}".format(statement.replace("\n", "")))


U_CID = 0
U_STEP = 1
U_FULL_NAME = 2
U_IS_BLOCKED = 3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def ct_users(self):
        sql = """
    CREATE TABLE Users (
        cid varchar(255) NOT NULL,
        step int NOT NULL DEFAULT 0,
        full_name varchar(255) NOT NULL,
        is_blocked int(1) NOT NULL DEFAULT 0,
        PRIMARY KEY (cid)
    );
    """

        try:
            self.execute(sql, commit=True)
        except:
            pass

    def add_user(self, cid, full_name):
        sql = """INSERT INTO Users(cid, full_name) VALUES(?, ?)"""
        self.execute(sql, parameters=(cid, full_name), commit=True)

    def select_users_all_ids(self):
        return self.execute("SELECT cid FROM Users WHERE is_blocked=0;", fetchall=True)

    def user_select(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def count_active_users(self):
        return self.execute("SELECT COUNT(*) FROM Users WHERE is_blocked=0;", fetchone=True)

    def select_user_all(self):
        return self.execute('SELECT * FROM Users;', fetchall=True)

    def select_user_all_body(self):
        return self.execute('SELECT cid, full_name, is_blocked FROM Users;', fetchall=True)

    def update_user_block(self, is_blocked, cid):
        sql = f"""UPDATE Users SET is_blocked=? WHERE cid=?;"""
        return self.execute(sql, parameters=(is_blocked, cid), commit=True)

    def delete_user(self, cid):
        return self.execute(f'DELETE FROM Users WHERE cid=?', parameters=(cid,), commit=True)

    def drop_table(self, name):
        try:
            return self.execute(f"DROP TABLE {name}", commit=True)
        except:
            return "Jadval mavjud emas!"


db = Database()

db.ct_users()
