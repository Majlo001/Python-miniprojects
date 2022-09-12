import sqlite3


class TodoDatabase(object):
    DB_LOCATION = 'todo_list.db'

    def __init__(self):
        self.conn = sqlite3.connect(TodoDatabase.DB_LOCATION)
        self.cur = self.conn.cursor()
        self.create_database()

    def create_database(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS todo_list (list_item text)""")
        self.conn.commit()
    
    def fetch(self):
        self.cur.execute("""SELECT * FROM todo_list""")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, data):
        self.cur.execute("""INSERT INTO todo_list VALUES (?) """, (data,))
        self.conn.commit()

    def remove_all(self):
        self.cur.execute("""DELETE * FROM todo_list""")
        self.conn.commit()

    def __exit__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


db = TodoDatabase()
# db.insert("Cook lunch")
# db.insert("Do homework")
# db.insert("Program in Python")
print(db.fetch())