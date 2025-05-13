import sqlite3

class DatabaseManager:
    def __init__(self, db_name='books.db'):
        self.conn = sqlite3.connect(db_name)
        self._initialize_db()
    
    def _initialize_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS books
                    (isbn TEXT, prices TEXT, score REAL, final_price REAL)''')
        self.conn.commit()
    
    def save_record(self, data: dict):
        c = self.conn.cursor()
        c.execute("INSERT INTO books VALUES (?,?,?,?)",
                 (data['isbn'], str(data['prices']), 
                  data['score'], data['final_price']))
        self.conn.commit()
    
    def get_records(self, limit=10):
        c = self.conn.cursor()
        c.execute("SELECT * FROM books ORDER BY rowid DESC LIMIT ?", (limit,))
        columns = [col[0] for col in c.description]
        return [dict(zip(columns, row)) for row in c.fetchall()]