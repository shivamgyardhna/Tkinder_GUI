import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDENT MANAGEMENT SYSTEM")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # Initialize database
        self.db = Database()
        if not self.db.connect(
            host="localhost",
            database="library_db",
            user="postgres",
            password="root",  # Change this
            port="5432"
        ):
            messagebox.showerror("Database Error", "Could not connect to database!")
            self.root.destroy()
            return
        
        # Variable to store selected student ID
        self.selected_id = None
        
        # Create GUI
        self.create_widgets()
        self.load_students()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # ===== TITLE =====
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill="x")
        
        title_label = tk.Label(
            title_frame,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # ===== INPUT FRAME =====
        input_frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Row 1: Name and Roll No
        row1 = tk.Frame(input_frame, bg="#ecf0f1")
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="Name:", font=("Arial", 11), bg="#ecf0f1", width=10, anchor="w").pack(side="left")
        self.name_entry = tk.Entry(row1, font=("Arial", 11), width=20)
        self.name_entry.pack(side="left", padx=5)
        
        tk.Label(row1, text="Roll No:", font=("Arial", 11), bg="#ecf0f1", width=10, anchor="w").pack(side="left", padx=(20, 0))
        self.roll_entry = tk.Entry(row1, font=("Arial", 11), width=15)
        self.roll_entry.pack(side="left", padx=5)
        
        # Row 2: Gender
        row2 = tk.Frame(input_frame, bg="#ecf0f1")
        row2.pack(fill="x", pady=5)
        
        tk.Label(row2, text="Gender:", font=("Arial", 11), bg="#ecf0f1", width=10, anchor="w").pack(side="left")
        self.gender_var = tk.StringVar(value="Male")
        tk.Radiobutton(row2, text="Male", variable=self.gender_var, value="Male", font=("Arial", 10), bg="#ecf0f1").pack(side="left")
        tk.Radiobutton(row2, text="Female", variable=self.gender_var, value="Female", font=("Arial", 10), bg="#ecf0f1").pack(side="left", padx=10)
        
        # Row 3: Course
        row3 = tk.Frame(input_frame, bg="#ecf0f1")
        row3.pack(fill="x", pady=5)
        
        tk.Label(row3, text="Course:", font=("Arial", 11), bg="#ecf0f1", width=10, anchor="w").pack(side="left")
        self.course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(
            row3,
            textvariable=self.course_var,
            values=["B.Tech", "M.Tech", "BCA", "MCA", "B.Sc", "M.Sc", "MBA"],
            font=("Arial", 11),
            state="readonly",
            width=18
        )
        course_dropdown.pack(side="left", padx=5)
        course_dropdown.current(0)  # Set default selection
        
        # ===== BUTTON FRAME =====
        button_frame = tk.Frame(self.root, bg="#ecf0f1", pady=10)
        button_frame.pack(fill="x", padx=10)
        
        btn_style = {"font": ("Arial", 11, "bold"), "width": 10, "height": 1, "cursor": "hand2"}
        
        tk.Button(button_frame, text="Add", bg="#27ae60", fg="white", command=self.add_student, **btn_style).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update", bg="#2980b9", fg="white", command=self.update_student, **btn_style).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete", bg="#e74c3c", fg="white", command=self.delete_student, **btn_style).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear", bg="#95a5a6", fg="white", command=self.clear_fields, **btn_style).pack(side="left", padx=5)
        
        # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.root, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbar
        scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        
        # Treeview (Table)
        self.student_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Roll No", "Gender", "Course"),
            yscrollcommand=scroll_y.set,
            selectmode="browse",
            height=12
        )
        scroll_y.config(command=self.student_table.yview)
        
        # Define column headings
        self.student_table.heading("ID", text="ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Roll No", text="Roll No")
        self.student_table.heading("Gender", text="Gender")
        self.student_table.heading("Course", text="Course")
        
        # Define column widths
        self.student_table.column("#0", width=0, stretch=False)  # Hide first column
        self.student_table.column("ID", width=50, anchor="center")
        self.student_table.column("Name", width=200, anchor="w")
        self.student_table.column("Roll No", width=120, anchor="center")
        self.student_table.column("Gender", width=100, anchor="center")
        self.student_table.column("Course", width=150, anchor="center")
        
        self.student_table.pack(fill="both", expand=True)
        
        # Bind table row selection
        self.student_table.bind("<ButtonRelease-1>", self.get_selected_row)
        
        # Apply custom styling to Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#34495e", foreground="white")
        style.map("Treeview", background=[("selected", "#3498db")])
    
    def load_students(self):
        """Load all students from database into table"""
        # Clear existing rows
        for row in self.student_table.get_children():
            self.student_table.delete(row)
        
        # Fetch and insert data
        students = self.db.fetch_all_students()
        for student in students:
            self.student_table.insert("", "end", values=student)
    
    def add_student(self):
        """Add new student to database"""
        name = self.name_entry.get().strip()
        roll_no = self.roll_entry.get().strip()
        gender = self.gender_var.get()
        course = self.course_var.get()
        
        # Validation
        if not name or not roll_no:
            messagebox.showerror("Input Error", "Name and Roll No are required!")
            return
        
        # Insert into database
        success, message = self.db.insert_student(name, roll_no, gender, course)
        
        if success:
            messagebox.showinfo("Success", message)
            self.load_students()
            self.clear_fields()
        else:
            messagebox.showerror("Error", message)
    
    def update_student(self):
        """Update selected student"""
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a student to update!")
            return
        
        name = self.name_entry.get().strip()
        roll_no = self.roll_entry.get().strip()
        gender = self.gender_var.get()
        course = self.course_var.get()
        
        # Validation
        if not name or not roll_no:
            messagebox.showerror("Input Error", "Name and Roll No are required!")
            return
        
        # Update in database
        success, message = self.db.update_student(self.selected_id, name, roll_no, gender, course)
        
        if success:
            messagebox.showinfo("Success", message)
            self.load_students()
            self.clear_fields()
        else:
            messagebox.showerror("Error", message)
    
    def delete_student(self):
        """Delete selected student"""
        if not self.selected_id:
            messagebox.showerror("Selection Error", "Please select a student to delete!")
            return
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
        if confirm:
            success, message = self.db.delete_student(self.selected_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_students()
                self.clear_fields()
            else:
                messagebox.showerror("Error", message)
    
    def get_selected_row(self, event):
        """Get selected row from table and populate fields"""
        try:
            selected_item = self.student_table.selection()[0]
            values = self.student_table.item(selected_item, "values")
            
            # Populate fields
            self.selected_id = values[0]
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, values[1])
            self.roll_entry.delete(0, "end")
            self.roll_entry.insert(0, values[2])
            self.gender_var.set(values[3])
            self.course_var.set(values[4])
        except IndexError:
            pass
    
    def clear_fields(self):
        """Clear all input fields"""
        self.name_entry.delete(0, "end")
        self.roll_entry.delete(0, "end")
        self.gender_var.set("Male")
        self.course_var.set("B.Tech")
        self.selected_id = None
    
    def on_closing(self):
        """Handle window close event"""
        self.db.close()
        self.root.destroy()

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
