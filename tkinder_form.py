import tkinter as tk
from tkinter import messagebox

def submit_form():
    name = name_entry.get()
    email = email_entry.get()
    gender = gender_var.get()
    b = branch_var.get()
    if name and email:
        messagebox.showinfo("Success", f"Name: {name}\nEmail: {email}\nGender: {gender}\nBranch: {b}")
    else:
        messagebox.showerror("Error", "Please fill all fields!")
    # Clear the form fields after submission
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    gender_var.set("Male")
    

root = tk.Tk()
root.title("Registration Form")
root.geometry("500x500")

tk.Label(root, text="Name:", font=("Arial", 12)).pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

tk.Label(root, text="Email:", font=("Arial", 12)).pack(pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.pack(pady=5)

tk.Label(root, text="Gender:", font=("Arial", 12)).pack(pady=5)
gender_var = tk.StringVar()
gender_var.set("Male")
gender_frame = tk.Frame(root)
gender_frame.pack(pady=5)

tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side="left", padx=10)
tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side="left", padx=10)


#branch field in form
tk.Label(root, text="Branch:", font=("Arial", 12)).pack(pady=5)
branch_var = tk.StringVar()
branch_var.set("CSE")
branch_frame = tk.Frame(root)
branch_frame.pack(pady=5)

tk.Radiobutton(branch_frame, text="CSE", variable=branch_var, value="CSE").pack(side="left", padx=10)
tk.Radiobutton(branch_frame, text="ECE", variable=branch_var, value="ECE").pack(side="left", padx=10)
tk.Radiobutton(branch_frame, text="ME", variable=branch_var, value="ME").pack(side="left", padx=10)
tk.Radiobutton(branch_frame, text="CE", variable=branch_var, value="CE").pack(side="left", padx=10)
submit_btn = tk.Button(root, 
                       text="Submit", 
                       command=submit_form,
                       bg="green",
                       fg="white",
                       font=("Arial", 12, "bold"),
                       padx=20,
                       pady=5)
submit_btn.pack(pady=20)

root.mainloop()