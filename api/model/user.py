import sqlite3

class User:
    def __init__(self, _id, username, password):
        super().__init__()
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):

        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE username=?"

            result = cursor.execute(query, (username,))

            row = result.fetchone()

            if row:
                user = cls(*row)
            else:
                user = None     

            return user
