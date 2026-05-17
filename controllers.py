class AuthSystem:
    def __init__(self, db_manager):
        self.db = db_manager

    def login(self, user_id, password):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT role, full_name FROM users WHERE user_id=? AND password=?", (user_id, password))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return {"role": user_data[0], "name": user_data[1]}
        return None


class SessionManager:
    def __init__(self):
        self.current_user_id = None
        self.current_user_name = None
        self.current_user_role = None

    def set_user(self, user_id, name, role):
        self.current_user_id = user_id
        self.current_user_name = name
        self.current_user_role = role

    def clear_session(self):
        self.current_user_id = None
        self.current_user_name = None
        self.current_user_role = None


class AttendanceManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_student_records(self, student_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT date, course_name, status FROM attendance WHERE student_id=? ORDER BY course_name, date",
                       (student_id,))
        records = cursor.fetchall()
        conn.close()
        return records

    def get_reports(self, role, user_id=None):
        conn = self.db.connect()
        cursor = conn.cursor()

        if role == 'admin':
            cursor.execute('''
                           SELECT a.date, a.student_id, u.full_name, a.course_name, a.status
                           FROM attendance a
                                    JOIN users u ON a.student_id = u.user_id
                           ORDER BY a.course_name, a.date
                           ''')
        elif role == 'instructor':
            cursor.execute('''
                           SELECT a.date, a.student_id, u.full_name, a.course_name, a.status
                           FROM attendance a
                                    JOIN users u ON a.student_id = u.user_id
                                    JOIN courses c ON a.course_name = c.course_name
                           WHERE c.instructor_id = ?
                           ORDER BY a.course_name, a.date
                           ''', (user_id,))

        records = cursor.fetchall()
        conn.close()
        return records


class CourseManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_all_courses(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT course_name FROM courses")
        courses = [row[0] for row in cursor.fetchall()]
        conn.close()
        return courses if courses else ["Course could not found"]

    def get_instructor_courses(self, instructor_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT course_name FROM courses WHERE instructor_id=?", (instructor_id,))
        courses = [row[0] for row in cursor.fetchall()]
        conn.close()
        return courses if courses else ["Course could not found"]

    def get_enrolled_students(self, course_name):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute('''
                       SELECT u.user_id, u.full_name
                       FROM enrollments e
                                JOIN users u ON e.student_id = u.user_id
                       WHERE e.course_name = ?
                       ''', (course_name,))

        students = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
        conn.close()
        return students if students else ["There is no registered student"]


class AdminManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def add_user(self, user_id, full_name, password, role):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        kullanici_var_mi = cursor.fetchone()

        if kullanici_var_mi != None:
            conn.close()
            return False, "A user already exists with this ID"

        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (user_id, full_name, password, role))
        conn.commit()
        conn.close()
        return True, f"{role.capitalize()} succsessfully added."

    def add_course(self, course_name, instructor_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT role FROM users WHERE user_id=?", (instructor_id,))
        user = cursor.fetchone()
        if not user or user[0] != 'instructor':
            conn.close()
            return False, "This is not a valid instructor ID"

        cursor.execute("SELECT * FROM courses WHERE course_name=?", (course_name,))
        ders_var_mi = cursor.fetchone()
        if ders_var_mi != None:
            conn.close()
            return False, "This course already exists with this ID"

        cursor.execute("INSERT INTO courses VALUES (?, ?)", (course_name, instructor_id))
        conn.commit()
        conn.close()
        return True, "Courses and instructor assigned."

    def enroll_student(self, student_id, course_name):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT role FROM users WHERE user_id=?", (student_id,))
        user = cursor.fetchone()
        if not user or user[0] != 'student':
            conn.close()
            return False, "This is not a valid student ID"

        cursor.execute("SELECT * FROM enrollments WHERE student_id=? AND course_name=?", (student_id, course_name))
        kayit_var_mi = cursor.fetchone()
        if kayit_var_mi != None:
            conn.close()
            return False, "The student already enrolled in this course."

        cursor.execute("INSERT INTO enrollments VALUES (?, ?)", (student_id, course_name))
        conn.commit()
        conn.close()
        return True, "The student enrolled in this course."