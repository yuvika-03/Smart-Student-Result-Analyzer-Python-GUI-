import tkinter as tk
from tkinter import messagebox

# Data 
subjects = {}
all_students = {}
valid_grades = {"S", "A", "B", "C", "D", "E", "F"}
grade_point = {"S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "E": 5, "F": 0}

# Main Logic
def add_subject():
    subject = subject_entry.get().strip()
    credits = credits_entry.get().strip()
    grade = grade_entry.get().strip().upper()

    if subject == "" or credits == "" or grade == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    if subject in subjects:
        messagebox.showerror("Error", "Subject already added!")
        return

    if not credits.isdigit() or int(credits) <= 0:
        messagebox.showerror("Error", "Credits must be a positive number!")
        return

    if grade not in valid_grades:
        messagebox.showerror("Error", "Invalid grade!")
        return

    subjects[subject] = {"credits": int(credits), "grade": grade}
    subject_list.insert(tk.END, f"{subject} | Credits: {credits} | Grade: {grade}")
    messagebox.showinfo("Success", f"{subject} added successfully!")

    subject_entry.delete(0, tk.END)
    credits_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)


def calculate_result():
    if not subjects:
        messagebox.showerror("Error", "No subjects added!")
        return None, None

    total_credits = 0
    total_points = 0

    for subject in subjects:
        credits = subjects[subject]["credits"]
        grade = subjects[subject]["grade"]

        total_credits += credits
        total_points += credits * grade_point[grade]

        if grade == "F":
            return 0, "FAIL"

    gpa = total_points / total_credits
    if gpa < 5:
        return gpa, "FAIL"
    return gpa, "PASS"


def save_student():
    name = name_entry.get().strip()

    if name == "":
        messagebox.showerror("Error", "Enter student name!")
        return

    gpa, status = calculate_result()
    if status is None:
        return

    all_students[name] = {"subjects": subjects.copy(), "gpa": round(gpa, 2), "result": status}
    messagebox.showinfo("Saved", f"Student '{name}' saved successfully!")

    # Reset for next student
    subjects.clear()
    subject_list.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    gpa_label.config(text="GPA: --")
    result_label.config(text="Result: --")


def view_students():
    if not all_students:
        messagebox.showinfo("Info", "No students saved yet")
        return

    window = tk.Toplevel(root)
    window.title("All Students")
    window.geometry("500x400")

    text = tk.Text(window, width=60, height=20)
    text.pack(padx=10, pady=10)

    for name, data in all_students.items():
        text.insert(tk.END, f"Student Name: {name}\n")

        for subject, details in data["subjects"].items():
            text.insert(tk.END, f"{subject} → Credits: {details['credits']}, Grade: {details['grade']}\n")

        text.insert(tk.END, f"   GPA: {data['gpa']}\n")
        text.insert(tk.END, f"   Result: {data['result']}\n")
        text.insert(tk.END, "-" * 50 + "\n")

    text.config(state="disabled")


def show_result():
    gpa, status = calculate_result()

    if status is None:
        return

    gpa_label.config(text=f"GPA: {round(gpa, 2)}")
    result_label.config(text=f"Result: {status}")

    if status == "PASS":
        result_label.config(fg="green")
    else:
        result_label.config(fg="red")


# Create window
root = tk.Tk()
root.title("Smart Student Result Analyzer")
root.geometry("800x600")
root.resizable(False, False)

heading = tk.Label(root, text="Smart Student Result Analyzer", font=("Arial", 16, "bold"))
heading.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Student Name:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
name_entry = tk.Entry(frame, width=30)
name_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Subject Name:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
subject_entry = tk.Entry(frame, width=30)
subject_entry.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Credits:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
credits_entry = tk.Entry(frame, width=30)
credits_entry.grid(row=2, column=1, pady=5)

tk.Label(frame, text="Grade:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
grade_entry = tk.Entry(frame, width=30)
grade_entry.grid(row=3, column=1, pady=5)

# Add Button
tk.Button(root, text="Add Subject", width=25, command=add_subject).pack(pady=8)
tk.Button(root, text="Calculate Result", width=25, command=show_result).pack(pady=8)
tk.Button(root, text="Save Student", width=25, command=save_student).pack(pady=8)
tk.Button(root, text="View All Students", width=25, command=view_students).pack(pady=8)
tk.Label(root, text="Added Subjects", font=("Arial", 12, "bold")).pack(pady=5)

subject_list = tk.Listbox(root, width=55, height=6)
subject_list.pack(pady=5)

gpa_label = tk.Label(root, text="GPA: --", font=("Arial", 12, "bold"))
gpa_label.pack(pady=5)

result_label = tk.Label(root, text="Result: --", font=("Arial", 12, "bold"))
result_label.pack(pady=5)

root.mainloop()