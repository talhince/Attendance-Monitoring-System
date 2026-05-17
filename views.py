import customtkinter as ctk
import datetime
from controllers import AuthSystem, SessionManager, AttendanceManager, CourseManager, AdminManager


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, auth_system, session_manager, navigate_callback):
        super().__init__(parent)
        self.auth_system = auth_system
        self.session = session_manager
        self.navigate = navigate_callback

        self.title_label = ctk.CTkLabel(self, text="Login Panel", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=40)

        self.id_entry = ctk.CTkEntry(self, placeholder_text="ID Number", width=200)
        self.id_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=200)
        self.password_entry.pack(pady=10)

        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.pack(pady=5)

        self.login_btn = ctk.CTkButton(self, text="Login", command=self.attempt_login)
        self.login_btn.pack(pady=20)

    def attempt_login(self):

        user_id = self.id_entry.get().strip()
        password = self.password_entry.get().strip()


        if user_id == "" or password == "":
            self.message_label.configure(text="ID and Password cannot be empty!", text_color="red")
            return

        user_info = self.auth_system.login(user_id, password)

        if user_info:
            self.session.set_user(user_id, user_info['name'], user_info['role'])
            if user_info['role'] == 'student':
                self.navigate("StudentDashboard")
            elif user_info['role'] == 'instructor':
                self.navigate("InstructorDashboard")
            elif user_info['role'] == 'admin':
                self.navigate("AdminDashboard")

            self.id_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.message_label.configure(text="")
        else:
            self.message_label.configure(text="Wrong ID or Password", text_color="red")


class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, session_manager, admin_manager, course_manager, navigate_callback):
        super().__init__(parent)
        self.session = session_manager
        self.admin_manager = admin_manager
        self.course_manager = course_manager
        self.navigate = navigate_callback

        self.header = ctk.CTkLabel(self, text="Root Panel", font=("Arial", 20, "bold"))
        self.header.pack(pady=10)

        self.message_lbl = ctk.CTkLabel(self, text="")
        self.message_lbl.pack()

        self.view_reports_btn = ctk.CTkButton(self, text="Show Reports", command=self.go_to_reports)
        self.view_reports_btn.pack(pady=5)

        self.tabview = ctk.CTkTabview(self, width=400, height=250)
        self.tabview.pack(pady=10)

        self.tab_user = self.tabview.add("Add User")
        self.tab_course = self.tabview.add("Add Course")
        self.tab_enroll = self.tabview.add("Course Registration")

        self.setup_user_tab()
        self.setup_course_tab()
        self.setup_enroll_tab()

        self.logout_btn = ctk.CTkButton(self, text="Log out", fg_color="red", command=self.logout)
        self.logout_btn.pack(pady=10)

    def go_to_reports(self):
        self.navigate("ReportFrame")

    def setup_user_tab(self):
        self.u_id = ctk.CTkEntry(self.tab_user, placeholder_text="New ID")
        self.u_id.pack(pady=5)
        self.u_name = ctk.CTkEntry(self.tab_user, placeholder_text="Name Surname")
        self.u_name.pack(pady=5)
        self.u_pass = ctk.CTkEntry(self.tab_user, placeholder_text="Password")
        self.u_pass.pack(pady=5)
        self.u_role = ctk.CTkOptionMenu(self.tab_user, values=["student", "instructor"])
        self.u_role.pack(pady=5)
        ctk.CTkButton(self.tab_user, text="Add", command=self.add_user).pack(pady=10)

    def setup_course_tab(self):
        self.c_name = ctk.CTkEntry(self.tab_course, placeholder_text="Course Name")
        self.c_name.pack(pady=10)
        self.c_inst = ctk.CTkEntry(self.tab_course, placeholder_text="Instructor ID")
        self.c_inst.pack(pady=10)
        ctk.CTkButton(self.tab_course, text="Create course", command=self.add_course).pack(pady=10)

    def setup_enroll_tab(self):
        self.e_student = ctk.CTkEntry(self.tab_enroll, placeholder_text="Student ID")
        self.e_student.pack(pady=10)
        self.e_course_var = ctk.StringVar(value="")
        self.e_course_menu = ctk.CTkOptionMenu(self.tab_enroll, variable=self.e_course_var, values=[""])
        self.e_course_menu.pack(pady=10)
        ctk.CTkButton(self.tab_enroll, text="Register Student", command=self.enroll_student).pack(pady=10)

    def load_data(self):
        courses = self.course_manager.get_all_courses()
        self.e_course_menu.configure(values=courses)
        self.e_course_var.set(courses[0])

    def show_message(self, success, text):
        color = "green" if success else "red"
        self.message_lbl.configure(text=text, text_color=color)

    def add_user(self):
        u_id_val = self.u_id.get().strip()
        u_name_val = self.u_name.get().strip()
        u_pass_val = self.u_pass.get().strip()
        u_role_val = self.u_role.get()


        if u_id_val == "" or u_name_val == "" or u_pass_val == "":
            self.show_message(False, "Fields cannot be empty!")
            return

        success, msg = self.admin_manager.add_user(u_id_val, u_name_val, u_pass_val, u_role_val)
        self.show_message(success, msg)

        if success:
            self.u_id.delete(0, 'end')
            self.u_name.delete(0, 'end')
            self.u_pass.delete(0, 'end')

    def add_course(self):
        c_name_val = self.c_name.get().strip()
        c_inst_val = self.c_inst.get().strip()

        if c_name_val == "" or c_inst_val == "":
            self.show_message(False, "Fields cannot be empty!")
            return

        success, msg = self.admin_manager.add_course(c_name_val, c_inst_val)
        self.show_message(success, msg)

        if success:
            self.c_name.delete(0, 'end')
            self.c_inst.delete(0, 'end')
            self.load_data()

    def enroll_student(self):
        e_student_val = self.e_student.get().strip()
        e_course_val = self.e_course_var.get()


        if e_student_val == "" or e_course_val == "" or e_course_val == "Course could not found":
            self.show_message(False, "Fields cannot be empty or invalid course!")
            return

        success, msg = self.admin_manager.enroll_student(e_student_val, e_course_val)
        self.show_message(success, msg)

        if success:
            self.e_student.delete(0, 'end')

    def logout(self):
        self.session.clear_session()
        self.navigate("LoginFrame")


class StudentDashboard(ctk.CTkFrame):
    def __init__(self, parent, session_manager, attendance_manager, navigate_callback):
        super().__init__(parent)
        self.session = session_manager
        self.attendance_manager = attendance_manager
        self.navigate = navigate_callback

        self.welcome_label = ctk.CTkLabel(self, text="Welcome Student Panel", font=("Arial", 20, "bold"))
        self.welcome_label.pack(pady=20)

        self.records_textbox = ctk.CTkTextbox(self, width=500, height=200, font=("Consolas", 12))
        self.records_textbox.pack(pady=10)

        self.logout_btn = ctk.CTkButton(self, text="Log out", command=self.logout, fg_color="red")
        self.logout_btn.pack(pady=20)

    def load_data(self):
        self.welcome_label.configure(text=f"Welcome, {self.session.current_user_name}")
        self.records_textbox.delete("0.0", "end")
        records = self.attendance_manager.get_student_records(self.session.current_user_id)
        if not records:
            self.records_textbox.insert("0.0", "You do not have any attendance records\n")
        else:
            self.records_textbox.insert("end", f"{'Date':<15} | {'Courses':<25} | {'Status':<10}\n")
            self.records_textbox.insert("end", "-" * 60 + "\n")
            for r in records:
                course = (r[1][:22] + '...') if len(r[1]) > 22 else r[1]
                self.records_textbox.insert("end", f"{r[0]:<15} | {course:<25} | {r[2]:<10}\n")

    def logout(self):
        self.session.clear_session()
        self.navigate("LoginFrame")


class InstructorDashboard(ctk.CTkFrame):
    def __init__(self, parent, session_manager, navigate_callback):
        super().__init__(parent)
        self.session = session_manager
        self.navigate = navigate_callback

        self.welcome_label = ctk.CTkLabel(self, text="Instructor", font=("Arial", 20, "bold"))
        self.welcome_label.pack(pady=20)

        self.take_att_btn = ctk.CTkButton(self, text="Take attendance", command=self.go_to_take_attendance)
        self.take_att_btn.pack(pady=10)

        self.view_reports_btn = ctk.CTkButton(self, text="See reports", command=self.go_to_reports)
        self.view_reports_btn.pack(pady=10)

        self.logout_btn = ctk.CTkButton(self, text="Log out", command=self.logout, fg_color="red")
        self.logout_btn.pack(pady=30)

    def go_to_take_attendance(self):
        self.navigate("TakeAttendanceFrame")

    def go_to_reports(self):
        self.navigate("ReportFrame")

    def load_data(self):
        self.welcome_label.configure(text=f"Welcome, {self.session.current_user_name}")

    def logout(self):
        self.session.clear_session()
        self.navigate("LoginFrame")


class TakeAttendanceFrame(ctk.CTkFrame):
    def __init__(self, parent, db_manager, course_manager, session_manager, navigate_callback):
        super().__init__(parent)
        self.db = db_manager
        self.course_manager = course_manager
        self.session = session_manager
        self.navigate = navigate_callback

        self.title_label = ctk.CTkLabel(self, text="Create attendance records", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=15)

        self.message_label = ctk.CTkLabel(self, text="")
        self.message_label.pack()

        bugun = datetime.date.today().strftime("%Y-%m-%d")
        self.date_entry = ctk.CTkEntry(self, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.insert(0, bugun)
        self.date_entry.pack(pady=10)

        self.course_var = ctk.StringVar(value="")
        self.course_menu = ctk.CTkOptionMenu(self, variable=self.course_var, values=[""], command=self.update_students)
        self.course_menu.pack(pady=10)

        self.student_var = ctk.StringVar(value="")
        self.student_menu = ctk.CTkOptionMenu(self, variable=self.student_var, values=[""])
        self.student_menu.pack(pady=10)

        durumlar = ["Present", "Absent", "Late"]
        self.status_var = ctk.StringVar(value=durumlar[0])
        self.status_menu = ctk.CTkOptionMenu(self, variable=self.status_var, values=durumlar)
        self.status_menu.pack(pady=10)

        self.save_btn = ctk.CTkButton(self, text="Save", command=self.save_attendance)
        self.save_btn.pack(pady=20)

        self.back_btn = ctk.CTkButton(self, text="Go Back", command=self.go_back_to_dashboard, fg_color="gray")
        self.back_btn.pack(pady=5)

    def go_back_to_dashboard(self):
        self.navigate("InstructorDashboard")

    def load_data(self):
        dersler = self.course_manager.get_instructor_courses(self.session.current_user_id)
        self.course_menu.configure(values=dersler)
        self.course_var.set(dersler[0])
        self.update_students(dersler[0])
        self.message_label.configure(text="")

    def update_students(self, selected_course):

        if selected_course == "Course could not found":
            self.student_menu.configure(values=["There is no registered student"])
            self.student_var.set("There is no registered student")
            return

        ogrenciler = self.course_manager.get_enrolled_students(selected_course)
        self.student_menu.configure(values=ogrenciler)
        self.student_var.set(ogrenciler[0])

    def save_attendance(self):
        date_val = self.date_entry.get().strip()
        course_val = self.course_var.get()
        student_val = self.student_var.get()

        if date_val == "":
            self.message_label.configure(text="Date cannot be empty!", text_color="red")
            return

        if course_val == "" or course_val == "Course could not found":
            self.message_label.configure(text="Invalid course!", text_color="red")
            return

        if student_val == "" or student_val == "There is no registered student":
            self.message_label.configure(text="No students registered to the course!", text_color="red")
            return

        status = self.status_var.get()
        student_id = student_val.split(" - ")[0]

        success, msg = self.db.take_attendance(date_val, student_id, course_val, status)
        color = "green" if success else "red"
        self.message_label.configure(text=msg, text_color=color)


class ReportFrame(ctk.CTkFrame):
    def __init__(self, parent, db_manager, session_manager, attendance_manager, navigate_callback):
        super().__init__(parent)
        self.db = db_manager
        self.session = session_manager
        self.attendance_manager = attendance_manager
        self.navigate = navigate_callback

        self.title_label = ctk.CTkLabel(self, text="All attendance records", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)

        self.report_textbox = ctk.CTkTextbox(self, width=650, height=250, font=("Consolas", 12))
        self.report_textbox.pack(pady=10)

        self.refresh_btn = ctk.CTkButton(self, text="Refresh", command=self.load_reports)
        self.refresh_btn.pack(pady=10)

        self.back_btn = ctk.CTkButton(self, text="Go Back", command=self.go_back, fg_color="gray")
        self.back_btn.pack(pady=5)

    def load_reports(self):
        self.report_textbox.delete("0.0", "end")
        records = self.attendance_manager.get_reports(self.session.current_user_role, self.session.current_user_id)

        self.report_textbox.insert("end",
                                   f"{'Date':<12} | {'Student ID':<10} | {'Name':<20} | {'Courses':<20} | {'Status':<10}\n")
        self.report_textbox.insert("end", "-" * 85 + "\n")

        for r in records:
            name = (r[2][:17] + '...') if len(r[2]) > 17 else r[2]
            course = (r[3][:17] + '...') if len(r[3]) > 17 else r[3]
            self.report_textbox.insert("end", f"{r[0]:<12} | {r[1]:<10} | {name:<20} | {course:<20} | {r[4]:<10}\n")

    def go_back(self):
        if self.session.current_user_role == 'admin':
            self.navigate("AdminDashboard")
        else:
            self.navigate("InstructorDashboard")


class AppWindow(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()
        self.title("Attendance Monitoring System")
        self.geometry("750x550")

        self.db_manager = db_manager
        self.auth_system = AuthSystem(db_manager)
        self.session_manager = SessionManager()
        self.attendance_manager = AttendanceManager(db_manager)
        self.course_manager = CourseManager(db_manager)
        self.admin_manager = AdminManager(db_manager)

        self.frames = {}
        self.setup_frames()

    def setup_frames(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        for F in (LoginFrame, StudentDashboard, InstructorDashboard, AdminDashboard, TakeAttendanceFrame, ReportFrame):
            frame_name = F.__name__

            if frame_name == "LoginFrame":
                frame = F(self, self.auth_system, self.session_manager, self.show_frame)
            elif frame_name == "StudentDashboard":
                frame = F(self, self.session_manager, self.attendance_manager, self.show_frame)
            elif frame_name == "InstructorDashboard":
                frame = F(self, self.session_manager, self.show_frame)
            elif frame_name == "AdminDashboard":
                frame = F(self, self.session_manager, self.admin_manager, self.course_manager, self.show_frame)
            elif frame_name == "TakeAttendanceFrame":
                frame = F(self, self.db_manager, self.course_manager, self.session_manager, self.show_frame)
            elif frame_name == "ReportFrame":
                frame = F(self, self.db_manager, self.session_manager, self.attendance_manager, self.show_frame)

            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        if hasattr(frame, 'load_data'):
            frame.load_data()
        frame.tkraise()