# Mini student Record Management System
from typing import Dict, List, Tuple

#Data Store
students: Dict[str, Dict] = {
    "STU001" : {
        "name": "Job",
        "age": 20,
        "scores": [55, 66, 77],
        "courses": [ 'python', 'DataSci', 'DataEng'],
        "seat": (4, 7),
        "graduated": False,
    },
    "STU002" : {
        "name": "Job",
        "age": 20,
        "scores": [55, 66, 77],
        "courses": [ 'python', 'DataSci', 'DataEng'],
        "seat": (4, 8),
        "graduated": False,
    },
}
students["STU001"]['name']   

# Helper Functions##

def avg(scores: List[float]) -> float:
    return round(sum(scores)/len(scores), 2) if scores else 0.0

def student_exists(student_id: str) -> bool:
    return student_id in students

def format_student(student_id: str) -> str:
    s = students[student_id]
    return (
        f"\nId: {student_id}\n"
        f"Name: {s['name']}\n"
        f"Age: {s['age']}\n"
        f"Scores: {s['scores']} | Avg: {avg(s['scores'])}\n"
        f"Seat: Row: {s['seat'][0]}, Seat: {s['seat'][1]}\n"
        f"Courses: {s['courses']}\n"
        f"Graduated: {s['graduated']}"        
    )

# CRUD(create, read, update, delete)
def create_student(student_id, name, age, seat: Tuple[int, int]):
    if student_exists(student_id):
        print("This student already exists")
        return
    students[student_id] = {
        "name": name,
        "age": age,
        "scores": [],
        "courses": [],
        "seat": seat,
        "graduated": False
    }
    print(f"Student with id {student_id} has been successfully created")

    def read_student(student_id):
        if student_exists(student_id):
            print(format_student(student_id))
        else:
            print(f"No student with id {student_id} exists")

def update_students(student_id:str, name: str = None, age: int= None, seat: Tuple[int, int] = None, graduated: bool = None):
    if not student_exists(student_id):
        print(f"This student with id:{student_id} does not exist")
        return
    s = students[student_id]
    if name is not None and age is not None and seat is not None and graduated is not None:
        s['name'] = name
        s['age'] = age
        s['seat'] = seat
        s['graduated'] = graduated
        print(f"student with {student_id} has been updated")


    # if age is not None:
    #     s['age'] = age
    # if seat is not None:
    #     s['seat']


def delete_student(student_id):
    if student_exists(student_id):
        del students[student_id]
        print(f"Student with ID: {student_id} has been deleted successfully")
    else:
        print(f"student with Id: {student_id} does not exist")

def add_score(student_id, score):
    if not student_exists(student_id):
        print('this student does not exist')
        return
    if 0 <= score <= 100:
        students[student_id]['scores'].append(score)
        print(f"score has been added successfully and the new average is {avg[student_id]['scores']}")
    else:
        print("Values must not be below 0 or more than 100")


def remove_score(student_id, index):
    if not student_exists(student_id):
        print(' This student does not exist')
        return
    s = students[student_id]['score']
    if 0<= index <= len(s):
        removed = s.pop(index)
        print(f"Then value {removed} has been deleted successfully")
    else:
        print("Invalid score index")


def add_course(student_id, course):
    if not student_exists(student_id):
        print('This student does not exist')
        return
    students[student_id]['courses'].append(course)
    print(f'{course} has been added successfully')


def remove_course(student_id, index):
    if not student_exists(student_id):
        print('This student does not exist')
        return
    s = students[student_id]['courses']
    if 0<= index <= len(s):
        removed = s.pop(index)
        print(f'then value {removed} has been deleted successfully')
    else:
        print("Invalid score index")

def main():
    while True:
        print("\n=====Students System=====")
        print("=1) Create student")
        print("2) Read student")
        print("3) update student")
        print("4) Delete student")
        print("5) Add course or Remove course")
        print("6) Add score or Remove score")
        print("0 Exist")

        choice = int(input("Select an option: ").strip())

        if choice == 1:
            sid = input("ID: ").strip()
            name = input("name: ").strip()
            try:
                age = int(input("Age: ").strip())
                row = int(input("Row: ").strip())
                seat = int(input("seat_no: ").strip())
            except ValueError:
                print("Age/Seat values must be integers")

            create_student(sid, name, age, (row, seat))

        if choice == 2:
                sid = input("ID: ").strip()
            read_student(sid)

        if choice == 3:
            sid = input("ID: ").strip()  
            if not student_exist(sid):
                print("Not found")  

                print("You can skip if no new vlaues is availialble just input whewe you want changes")
            name = input("New name: ").strip()
            age = input("New age: ").strip()
            seat_row = input("New seat row: ").strip()
            seat_no = input("New seat no: ").strip()
            graduated = input("Graduated y/n: ")

            age = int(age) if age else None
            seat = (int(seat_row), int(seat_no)) if seat_row and seat_no else None

            if graduated == 'y':
                graduated = True
            elif graduated == 'n':
                graduated = False
            else:
                graduated = None
            update_students(sid, name, age, (seat_row, seat_no), graduated)

        elif choice == 4:
            sid = input("ID: ").strip()
            delete_student(sid)
        
        elif choice == 5:
            sid = input("ID: ").strip()
            if not student_exists(sid):
                print("Not found")
                continue
            sub = input("a. Add Course b. Remove course")
            if sub == "a":
                course = input("Name of new course")
                add_course(sid, course)
            elif sub == "b":
                try: 
                    idx = int(input("course index(0-based): ").strip())
                except ValueError:
                    print("index value must be an integer")
                    continue
                remove_course(sid, idx)
            else: 
                print("Option does not exist")

        elif choice == 6: 
            sid = input("ID: ").strip()
            if not student_exists(sid):
                print("Not found")
                continue
            sub = input("a. Add score b. Remove score")
            if sub == "a":
                try:
                    course = int(input("Score (0-100): ").strip())
                except ValueError:
                    print("score must be an integer")
                add_score(sid, course)
            elif sub == "b":
                try: 
                    idx = int(input("course index(0-based): ").strip())
                except ValueError:
                    print("index value must be an integer")
                    continue
                remove_score(sid, idx)
            else: 
                print("Option does not exist")\
            
        elif choice == 0:
            print("Goodbye")
            break

        else:
            print("Invalid option, try again")

if __name__ == "__main__":
    main()         
            

        
            