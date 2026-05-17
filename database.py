import sqlite3

class DatabaseManager:
    def __init__(self, db_name="attendance_system.db"):
        self.db_name = db_name
        self.setup_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def setup_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                student_id TEXT NOT NULL,
                course_name TEXT NOT NULL,
                status TEXT NOT NULL,
                UNIQUE (date, student_id, course_name)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_name TEXT PRIMARY KEY,
                instructor_id TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                student_id TEXT NOT NULL,
                course_name TEXT NOT NULL,
                UNIQUE (student_id, course_name)
            )
        """)

        cursor.execute("SELECT * FROM users WHERE user_id = 'admin'")
        admin_var_mi = cursor.fetchone()

        if admin_var_mi is None:
            cursor.execute("""
                INSERT INTO users (user_id, full_name, password, role)
                VALUES ('admin', 'System Admin', 'admin', 'admin')
            """)

        conn.commit()
        conn.close()

    def take_attendance(self, date, student_id, course_name, status):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM attendance 
            WHERE date=? AND student_id=? AND course_name=?
        """, (date, student_id, course_name))

        kayit_var_mi = cursor.fetchone()

        if kayit_var_mi is not None:
            conn.close()
            return False, "Attendance already entered for this student"

        cursor.execute("""
            INSERT INTO attendance (date, student_id, course_name, status)
            VALUES (?, ?, ?, ?)
        """, (date, student_id, course_name, status))

        conn.commit()
        conn.close()

        return True, "Attendance successfully recorded"