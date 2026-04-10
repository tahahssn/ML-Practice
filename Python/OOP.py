class Student:
    def __init__(self, name, age, gpa):
        self.name = str(name)
        self.age = int(age)
        self.gpa = float(gpa)
        print("Adding Data to Database...")

s1 = Student(input("Enter Your Name: "), input("Enter Your Age: "), input("Enter Your GPA: "))
print("Your Name is:", s1.name)
print("Your Age is:", s1.age)
print("Your GPA is:", s1.gpa)