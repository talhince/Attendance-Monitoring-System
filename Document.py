
#The main goal of this project is to digitize the manual attendance process, making it faster and more reliable.
#By using SQLite database, the system ensures that student records are stored securely and are easily accessible
#for reporting. It also aims to provide a user-friendly experience through a GUI while maintaining data integrity
#with role-based access control.

#The system is built around three distinct user roles, each with specific permissions only authorized personnel
#can perform specific actions within the system (e.g., only instructors can take attendance).

#General Features: The system automatically initializes the database and required tables. Users log in with a
#unique ID and password, and the system directs them to the appropriate dashboard based on their role.

#Admin Dashboard: The "Root" panel handles the core system setup. The Admin can register new students and
#instructors, create courses, and enroll students into specific classes.

#They also have the authority to view comprehensive attendance reports for the entire institution.
#Instructor Dashboard: Instructors manage the courses assigned to them. They can select a date and record
#attendance (Present, Absent, or Late) for students enrolled in their classes. They can also view historical
#reports for their own courses.

#Student Dashboard: Students have a "Read-Only" view. Once logged in, they can immediately see their personal
#attendance history, showing the date, course name, and their specific status for each session.

