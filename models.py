class User:
    def __init__(self, user_id, full_name, password, role):
        self.user_id = user_id
        self.full_name = full_name
        self.password = password
        self.role = role

class Student(User):
    def __init__(self, user_id, full_name, password):
        super().__init__(user_id, full_name, password, role='student')

class Instructor(User):
    def __init__(self, user_id, full_name, password):
        super().__init__(user_id, full_name, password, role='instructor')

class Admin(User):
    def __init__(self, user_id, full_name, password):
        super().__init__(user_id, full_name, password, role='admin')

class AttendanceRecord:
    def __init__(self, record_id, date, student_id, course_name, status):
        self.record_id = record_id
        self.date = date
        self.student_id = student_id
        self.course_name = course_name
        self.status = status