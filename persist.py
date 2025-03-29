import sqlite3 

def connect_db():
    conn = sqlite3.connect('phisingReports.db')
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            reason TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warningLevels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            from_idx INTEGER NOT NULL,
            to_idx INTEGER NOT NULL,
            FOREIGN KEY (report_id) REFERENCES reports (id)
        )
    ''')
    
    conn.commit()
    print("Successfully implemented databases")
    return

def insert_into_tables(sender, recipient, message, reason, source, warningRanges):
    if sender is None:
        raise ValueError("Sender can't be None")
    if recipient is None:
        raise ValueError("Recipient can't be None")
    if message is None:
        raise ValueError("Message can't be None")
    if reason is None:
        raise ValueError("Reason can't be None")
    if source is None:
        raise ValueError("source can't be None")
    if warningRanges is None:
        raise ValueError("warningRanges can't be None")
    
    conn = connect_db()
    create_tables(conn)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO reports (recipient, sender, message, reason)
            VALUES (?,?,?,?)
        ''', (recipient, sender, message, reason))
        
        report_id = cursor.lastrowid
        
        entiries = [(report_id, source, from_idx, to_idx) for from_idx, to_idx in warningRanges]
        
        cursor.executemany('''
            INSERT INTO warningLevels (report_id, source, from_idx, to_idx)
            VALUES (?,?,?,?)
        ''', entiries)
        
        conn.commit()
        print("Successfully committed entiries")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        conn.rollback()
    finally:
        conn.close()
    
if __name__ == "__main__":
    insert_into_tables(
        sender="123@gmail.com",
        recipient="456@gmail.com",
        message="Hello World",
        reason="Fake Message",
        source="message",
        warningRanges=[(1, 5), (10, 15), (20, 25)]
    )
    insert_into_tables(
        sender="789@gmail.com",
        recipient="999@gma1l.com",
        message="Benim adım Esat",
        reason="Fake email address",
        source="email",
        warningRanges=[(7,7)]
    )
    