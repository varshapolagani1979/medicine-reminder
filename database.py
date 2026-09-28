import sqlite3

DATABASE = "medicine_reminder.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            frequency TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_medicine(medicine_name, dosage, reminder_time, frequency):
    conn = get_connection()

    conn.execute("""
        INSERT INTO medicines
        (medicine_name, dosage, reminder_time, frequency)
        VALUES (?, ?, ?, ?)
    """, (
        medicine_name,
        dosage,
        reminder_time,
        frequency
    ))

    conn.commit()
    conn.close()


def get_medicines():
    conn = get_connection()

    medicines = conn.execute("""
        SELECT * FROM medicines
        ORDER BY reminder_time
    """).fetchall()

    conn.close()

    return medicines


def delete_medicine(medicine_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM medicines WHERE id = ?",
        (medicine_id,)
    )

    conn.commit()
    conn.close()