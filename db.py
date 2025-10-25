import psycopg2
from psycopg2 import Error

class Database:
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None
        
    def connect(self, host="localhost", database="library_db", user="postgres", password="root", port="5432"):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("✓ Successfully connected to PostgreSQL database")
            self.create_table()
            return True
        except Error as e:
            print(f"✗ Error connecting to PostgreSQL: {e}")
            return False
    
    def create_table(self):
        """Create students table if it doesn't exist"""
        try:
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    roll_no VARCHAR(20) UNIQUE NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    course VARCHAR(50) NOT NULL
                )
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("✓ Students table ready")
        except Error as e:
            print(f"✗ Error creating table: {e}")
    
    def insert_student(self, name, roll_no, gender, course):
        """Insert a new student (CREATE)"""
        try:
            insert_query = '''
                INSERT INTO students (name, roll_no, gender, course) 
                VALUES (%s, %s, %s, %s)
            '''
            self.cursor.execute(insert_query, (name, roll_no, gender, course))
            self.connection.commit()
            return True, "Student added successfully!"
        except psycopg2.IntegrityError:
            self.connection.rollback()
            return False, "Roll number already exists!"
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {e}"
    
    def fetch_all_students(self):
        """Fetch all students (READ)"""
        try:
            select_query = "SELECT * FROM students ORDER BY id"
            self.cursor.execute(select_query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Error fetching students: {e}")
            return []
    
    def update_student(self, student_id, name, roll_no, gender, course):
        """Update student details (UPDATE)"""
        try:
            update_query = '''
                UPDATE students 
                SET name = %s, roll_no = %s, gender = %s, course = %s 
                WHERE id = %s
            '''
            self.cursor.execute(update_query, (name, roll_no, gender, course, student_id))
            self.connection.commit()
            return True, "Student updated successfully!"
        except psycopg2.IntegrityError:
            self.connection.rollback()
            return False, "Roll number already exists!"
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {e}"
    
    def delete_student(self, student_id):
        """Delete a student (DELETE)"""
        try:
            delete_query = "DELETE FROM students WHERE id = %s"
            self.cursor.execute(delete_query, (student_id,))
            self.connection.commit()
            return True, "Student deleted successfully!"
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {e}"
    
    def search_student(self, roll_no):
        """Search student by roll number"""
        try:
            search_query = "SELECT * FROM students WHERE roll_no = %s"
            self.cursor.execute(search_query, (roll_no,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"✗ Error searching student: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
