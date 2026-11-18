import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import customtkinter as ctk


DB_FILE = Path(__file__).with_name("academic_planner.db")


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(DB_FILE)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    def create_tables(self):
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            effort TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );
        """)
        self.connection.commit()

    def register(self, name, email, password):
        self.connection.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name.strip(), email.strip().lower(), password),
        )
        self.connection.commit()

    def login(self, email, password):
        return self.connection.execute(
            "SELECT id, name FROM users WHERE email = ? AND password = ?",
            (email.strip().lower(), password),
        ).fetchone()

    def add_course(self, user_id, name):
        self.connection.execute(
            "INSERT INTO courses (user_id, name) VALUES (?, ?)",
            (user_id, name.strip()),
        )
        self.connection.commit()

    def get_courses(self, user_id):
        return self.connection.execute(
            "SELECT id, name FROM courses WHERE user_id = ? ORDER BY name",
            (user_id,),
        ).fetchall()

    def add_assignment(self, user_id, course_id, title, due_date, effort):
        self.connection.execute(
            "INSERT INTO assignments (user_id, course_id, title, due_date, effort) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, course_id, title.strip(), due_date, effort.strip()),
        )
        self.connection.commit()

    def get_assignments(self, user_id, start=None, end=None):
        query = """
            SELECT a.id, c.name, a.title, a.due_date, a.effort
            FROM assignments a
            JOIN courses c ON c.id = a.course_id
            WHERE a.user_id = ?
        """
        params = [user_id]
        if start and end:
            query += " AND a.due_date >= ? AND a.due_date <= ?"
            params.extend([start, end])
        query += " ORDER BY a.due_date, a.title"
        return self.connection.execute(query, params).fetchall()


class AuthFrame(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.db = master.db
        self.on_success = on_success

        card = ctk.CTkFrame(self, width=420, corner_radius=18)
        card.pack(expand=True)

        ctk.CTkLabel(card, text="Academic Planner", font=("Arial", 28, "bold")).pack(pady=(35, 5))
        ctk.CTkLabel(card, text="Plan courses and assignments", text_color="gray").pack(pady=(0, 24))

        self.mode = ctk.CTkSegmentedButton(
            card,
            values=["Login", "Register"],
            command=self.change_mode,
        )
        self.mode.set("Login")
        self.mode.pack(padx=40, fill="x")

        self.name_entry = ctk.CTkEntry(card, placeholder_text="Full name", width=340)
        self.email_entry = ctk.CTkEntry(card, placeholder_text="Email", width=340)
        self.password_entry = ctk.CTkEntry(card, placeholder_text="Password", show="*", width=340)

        self.email_entry.pack(pady=(24, 10), padx=40)
        self.password_entry.pack(pady=(0, 10), padx=40)

        self.message = ctk.CTkLabel(card, text="", text_color="#ff8b8b")
        self.message.pack(pady=5)

        self.submit = ctk.CTkButton(card, text="Log in", command=self.submit, width=340)
        self.submit.pack(pady=(5, 35), padx=40)

    def change_mode(self, mode):
        if mode == "Register":
            self.name_entry.pack(pady=(24, 10), padx=40)
            self.email_entry.pack(pady=(0, 10), padx=40)
            self.password_entry.pack(pady=(0, 10), padx=40)
            self.submit.configure(text="Create account")
        else:
            self.name_entry.pack_forget()
            self.submit.configure(text="Log in")
        self.message.configure(text="")

    def submit(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if self.mode.get() == "Register":
            name = self.name_entry.get().strip()
            if not name or not email or not password:
                self.message.configure(text="Please complete all fields.")
                return
            try:
                self.db.register(name, email, password)
                user = self.db.login(email, password)
                self.on_success(user)
            except sqlite3.IntegrityError:
                self.message.configure(text="An account with that email already exists.")
        else:
            user = self.db.login(email, password)
            if user:
                self.on_success(user)
            else:
                self.message.configure(text="Email or password is incorrect.")


class PlannerFrame(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master)
        self.db = master.db
        self.user_id, self.user_name = user
        self.week_start = date.today() - timedelta(days=date.today().weekday())

        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(sidebar, text="Academic Planner", font=("Arial", 18, "bold")).pack(pady=(25, 5), padx=15)
        ctk.CTkLabel(sidebar, text=f"{self.user_name}", text_color="gray").pack(pady=(0, 25))

        ctk.CTkButton(sidebar, text="Calendar", command=lambda: self.show_page("Calendar")).pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(sidebar, text="Courses", command=lambda: self.show_page("Courses"), fg_color="transparent").pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(sidebar, text="Assignments", command=lambda: self.show_page("Assignments"), fg_color="transparent").pack(padx=20, pady=5, fill="x")
        ctk.CTkButton(sidebar, text="Log out", command=master.show_auth, fg_color="#923d47", hover_color="#752f38").pack(side="bottom", padx=20, pady=20, fill="x")

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self.show_page("Calendar")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, page):
        if page == "Calendar":
            self.show_calendar()
        elif page == "Courses":
            self.show_courses()
        else:
            self.show_assignments()

    def show_calendar(self):
        self.clear_content()
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Weekly Calendar", font=("Arial", 24, "bold")).pack(side="left")

        nav = ctk.CTkFrame(header, fg_color="transparent")
        nav.pack(side="right")
        ctk.CTkButton(nav, text="←", width=40, command=lambda: self.move_week(-7)).pack(side="left", padx=3)
        ctk.CTkButton(nav, text="Today", width=70, command=self.go_today).pack(side="left", padx=3)
        ctk.CTkButton(nav, text="→", width=40, command=lambda: self.move_week(7)).pack(side="left", padx=3)

        week_end = self.week_start + timedelta(days=6)
        ctk.CTkLabel(
            self.content,
            text=f"{self.week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}",
            text_color="gray",
        ).pack(anchor="w", pady=(10, 12))

        assignments = self.db.get_assignments(
            self.user_id,
            self.week_start.isoformat(),
            week_end.isoformat(),
        )
        by_day = {self.week_start + timedelta(days=i): [] for i in range(7)}
        for assignment in assignments:
            due = date.fromisoformat(assignment[3])
            if due in by_day:
                by_day[due].append(assignment)

        grid = ctk.CTkFrame(self.content, fg_color="#20252d")
        grid.pack(fill="both", expand=True)
        for day_index, (day, items) in enumerate(by_day.items()):
            column = ctk.CTkFrame(grid, fg_color=("#f3f4f6", "#262b33"), corner_radius=8)
            column.grid(row=0, column=day_index, padx=4, pady=4, sticky="nsew")
            grid.grid_columnconfigure(day_index, weight=1)
            ctk.CTkLabel(column, text=day.strftime("%a").upper(), text_color="gray", font=("Arial", 12, "bold")).pack(pady=(10, 0))
            ctk.CTkLabel(column, text=str(day.day), font=("Arial", 20, "bold")).pack(pady=(0, 10))

            if not items:
                ctk.CTkLabel(column, text="—", text_color="gray").pack(pady=10)
            for _, course, title, _, effort in items:
                card = ctk.CTkFrame(column, fg_color="#3973ad", corner_radius=6)
                card.pack(fill="x", padx=6, pady=4)
                ctk.CTkLabel(card, text=title, font=("Arial", 12, "bold"), wraplength=150).pack(anchor="w", padx=8, pady=(7, 1))
                ctk.CTkLabel(card, text=course, text_color="#dbe8f5", wraplength=150).pack(anchor="w", padx=8)
                if effort:
                    ctk.CTkLabel(card, text=f"{effort}", text_color="#dbe8f5").pack(anchor="w", padx=8, pady=(1, 7))

    def move_week(self, days):
        self.week_start += timedelta(days=days)
        self.show_calendar()

    def go_today(self):
        self.week_start = date.today() - timedelta(days=date.today().weekday())
        self.show_calendar()

    def show_courses(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="My Courses", font=("Arial", 24, "bold")).pack(anchor="w")

        form = ctk.CTkFrame(self.content)
        form.pack(fill="x", pady=(15, 10))
        name_entry = ctk.CTkEntry(form, placeholder_text="Course name", width=300)
        name_entry.pack(side="left", padx=12, pady=12)

        message = ctk.CTkLabel(form, text="")
        message.pack(side="right", padx=12)

        def add_course():
            if not name_entry.get().strip():
                message.configure(text="Enter a course name.", text_color="#ff8b8b")
                return
            self.db.add_course(self.user_id, name_entry.get())
            name_entry.delete(0, "end")
            message.configure(text="Course added.", text_color="#79c89d")
            render_courses()

        ctk.CTkButton(form, text="Add Course", command=add_course).pack(side="right", padx=12)

        list_frame = ctk.CTkScrollableFrame(self.content)
        list_frame.pack(fill="both", expand=True)

        def render_courses():
            for widget in list_frame.winfo_children():
                widget.destroy()
            courses = self.db.get_courses(self.user_id)
            if not courses:
                ctk.CTkLabel(list_frame, text="No courses yet.", text_color="gray").pack(pady=30)
            for course_id, course_name in courses:
                row = ctk.CTkFrame(list_frame)
                row.pack(fill="x", pady=4)
                ctk.CTkLabel(row, text=course_name, font=("Arial", 16, "bold")).pack(side="left", padx=15, pady=12)

        render_courses()

    def show_assignments(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Assignments", font=("Arial", 24, "bold")).pack(anchor="w")

        courses = self.db.get_courses(self.user_id)
        if not courses:
            ctk.CTkLabel(self.content, text="Add a course before creating an assignment.", text_color="gray").pack(pady=30)
            return

        form = ctk.CTkFrame(self.content)
        form.pack(fill="x", pady=(15, 10))

        title_entry = ctk.CTkEntry(form, placeholder_text="Assignment title", width=220)
        title_entry.grid(row=0, column=0, padx=10, pady=12)
        course_menu = ctk.CTkOptionMenu(form, values=[name for _, name in courses])
        course_menu.grid(row=0, column=1, padx=10, pady=12)
        due_entry = ctk.CTkEntry(form, placeholder_text="Due date YYYY-MM-DD", width=170)
        due_entry.insert(0, date.today().isoformat())
        due_entry.grid(row=0, column=2, padx=10, pady=12)
        effort_entry = ctk.CTkEntry(form, placeholder_text="Effort (optional)", width=150)
        effort_entry.grid(row=0, column=3, padx=10, pady=12)

        message = ctk.CTkLabel(form, text="")
        message.grid(row=1, column=0, columnspan=4, pady=(0, 8))

        list_frame = ctk.CTkScrollableFrame(self.content)
        list_frame.pack(fill="both", expand=True)

        def render_assignments():
            for widget in list_frame.winfo_children():
                widget.destroy()
            assignments = self.db.get_assignments(self.user_id)
            if not assignments:
                ctk.CTkLabel(list_frame, text="No assignments yet.", text_color="gray").pack(pady=30)
            for _, course, title, due, effort in assignments:
                row = ctk.CTkFrame(list_frame)
                row.pack(fill="x", pady=4)
                ctk.CTkLabel(row, text=title, font=("Arial", 16, "bold")).pack(side="left", padx=15, pady=12)
                ctk.CTkLabel(row, text=f"{course}  •  Due {due}" + (f"  •  {effort}" if effort else ""), text_color="gray").pack(side="right", padx=15)

        def add_assignment():
            title = title_entry.get().strip()
            due = due_entry.get().strip()
            course_name = course_menu.get()
            course_id = next(course_id for course_id, name in courses if name == course_name)
            if not title:
                message.configure(text="Enter an assignment title.", text_color="#ff8b8b")
                return
            try:
                parsed_due = datetime.strptime(due, "%Y-%m-%d").date()
            except ValueError:
                message.configure(text="Use a valid date in YYYY-MM-DD format.", text_color="#ff8b8b")
                return
            self.db.add_assignment(self.user_id, course_id, title, parsed_due.isoformat(), effort_entry.get())
            title_entry.delete(0, "end")
            effort_entry.delete(0, "end")
            message.configure(text="Assignment added.", text_color="#79c89d")
            render_assignments()

        ctk.CTkButton(form, text="Add Assignment", command=add_assignment).grid(row=0, column=4, padx=10, pady=12)
        render_assignments()


class AcademicPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Academic Planner")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.db = Database()
        self.show_auth()

    def show_auth(self):
        for widget in self.winfo_children():
            widget.destroy()
        frame = AuthFrame(self, self.show_planner)
        frame.pack(fill="both", expand=True)

    def show_planner(self, user):
        for widget in self.winfo_children():
            widget.destroy()
        frame = PlannerFrame(self, user)
        frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = AcademicPlannerApp()
    app.mainloop()
