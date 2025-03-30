import sqlite3
import os
from src.db_types import _RawRecord, Record, Flag

DB_NAME = "data/phisingReport.db"
#DB_NAME = ":memory:"
REPORT_TABLE_NAME = "reports"
FLAG_TABLE_NAME = "flags"

class Factories:
    def _raw_record_factory(cursor, row):
        return _RawRecord(*row)
    
    def _flag_factory(cursor, row):
        return Flag(*row)

class DB:
    cursor: sqlite3.Cursor
    
    def __init__(self):
        db_exists = os.path.isfile(DB_NAME)
        self._conn = sqlite3.connect(DB_NAME)
        self.cursor = self._conn.cursor()

        if(not db_exists):
            self.createTable()

    def createTable(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {REPORT_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient TEXT NOT NULL,
                sender TEXT NOT NULL,
                body TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {FLAG_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_id INTEGER NOT NULL,
                source TEXT NOT NULL,
                from_idx INTEGER NOT NULL,
                to_idx INTEGER NOT NULL,
                reason TEXT NOT NULL,
                FOREIGN KEY (report_id) REFERENCES reports (id)
            )
        ''')
    
    def _pairFlags(self, report: _RawRecord) -> Record:
        cursor = self.cursor
        self._conn.row_factory = Factories._flag_factory
        flags: list[Flag] = cursor.execute(f"SELECT * FROM {FLAG_TABLE_NAME} WHERE report_id=?", (report[0],))
        
        self._conn.row_factory = None
        return Record(
            *report,
            flags
        )
    
    def select(self, id: int=None, sender: str=None) -> list[Record]:
        cursor = self.cursor
        self._conn.row_factory = Factories._raw_record_factory
        if(id):
            cursor.execute(f"SELECT * FROM {REPORT_TABLE_NAME} WHERE id=?", (id,))
            return [self._pairFlags(cursor.fetchone())]
        if(sender):
            cursor.execute(f"SELECT * FROM {REPORT_TABLE_NAME} WHERE sender=?", (sender,))
            return [self._pairFlags(cursor.fetchone())]
        
        cursor.execute(f"SELECT * FROM {REPORT_TABLE_NAME}")
        res: list[_RawRecord] = cursor.fetchall()
        print(res)
        reports = [ self._pairFlags(r) for r in res ]
        return reports
        
        

    def insert(self, sender: str, recipient: str, body: str, flags: list[Flag]) -> None:
        if sender is None:
            raise ValueError("Sender can't be None")
        if recipient is None:
            raise ValueError("Recipient can't be None")
        if body is None:
            raise ValueError("Message can't be None")
        if flags is None:
            raise ValueError("warningRanges can't be None")
        
        
        try:
            self.cursor.execute(f'''
                INSERT INTO {REPORT_TABLE_NAME} (recipient, sender, body)
                VALUES (?,?,?)
            ''', (recipient, sender, body))
            
            report_id: int = self.cursor.lastrowid
            
            entries = [(report_id, source, from_idx, to_idx, reason) for _, _, source, from_idx, to_idx, reason in flags]
            
            self.cursor.executemany(f'''
                INSERT INTO {FLAG_TABLE_NAME} (report_id, source, from_idx, to_idx, reason)
                VALUES (?,?,?,?,?)
            ''', entries)
            
            self._conn.commit()
            print("Successfully committed entiries")
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            self._conn.rollback()
        finally:
            self._conn.close()