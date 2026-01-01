valid_grades = {"S", "A", "B", "C", "D", "E", "F"}
grade_point = {"S":10, "A":9, "B":8, "C":7, "D":6, "E":5, "F":0}

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input! Enter a number.")

        

def add_subjects():
    num_of_entry = get_positive_integer("Number of Subjects: ")
    subjects = {}

    for i in range(num_of_entry):
        print(f"\nAdding subject {i+1}")

        while True:
            subject = input("Enter the subject:").strip()
            if subject == "":
                print("Subject name cannot be empty.")
            elif subject in subjects:
                print("Subject already exists. Enter a different subject.")
            else:
                break
                
        credits = get_positive_integer("Credits: ")
                        
        while True:
            grade = input("Grade: ").strip().upper()
            if grade in valid_grades:
                break
            else:
                print("Invalid grade!")
                        
        subjects[subject] = {"credits": credits, "grade": grade}
        print("Subject added successfully!")
    return subjects


def calculate_gpa(subjects):
    total_credits = 0
    total_points = 0

    for subject in subjects:
        credits = subjects[subject]["credits"]
        grade = subjects[subject]["grade"]

        total_credits += credits
        total_points += credits * grade_point[grade]

    if total_credits == 0:
        return 0

    return total_points / total_credits


def check_result(subjects, gpa):
    for subject in subjects:
        if subjects[subject]["grade"] == "F":
            return "FAIL"
    
    if gpa<5:
        return "FAIL"
    
    return "PASS"


def display_result(name, subjects, gpa, status):
    result = f"\nStudent Name: {name}\n"

    for subject in subjects:
        result += f"{subject} ---> Credits: {subjects[subject]['credits']}, Grade: {subjects[subject]['grade']}\n"

    result += f"GPA: {round(gpa, 2)}\n"
    result += f"Result: {status}\n"

    print(result)
    return result


def main():
    filename = "Students_results.txt"

    with open(filename, "w") as file:
        while True:
            while True:
                name = input("Enter your name: ").strip()
                if name:
                    break
                print("Name cannot be empty.")

            subjects = add_subjects()
            gpa = calculate_gpa(subjects)
            status = check_result(subjects, gpa)

            result_str = display_result(name, subjects, gpa, status)
            file.write(result_str + "\n")

            choice = input("Add another student? (y/n): ").lower()
            if choice != "y":
                break

    print(f"\nAll results saved in {filename}")
    
if __name__ == "__main__":
    main()