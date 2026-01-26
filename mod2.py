'''Module 2 — Core Campus Logic
Purpose: Represent the real campus operations.
This module may include:
Courses, records, services, assets, or bookings
Business rules (enroll, assign, calculate, approve, pay)
Data validation and constraints
This is the core logic of PCOS.
If this module is weak, the system is meaningless.'''

from module2 import run_business_rule_tests


def validate_email(email):  
    if not email or "@" not in email:
        return False
    return True

def validate_student_email(email):
    if not email or "@" not in email:
        return False, "Invalid email!"
    domain = email.split("@")[-1]
    if domain.lower() != "picos.edu":
        return False, "Invalid email domain!"
    return True, "Valid email"  

def validate_student_id(student_id):
    if not student_id or len(student_id) != 15 or not student_id.startswith("PCOS"):
        return False, "Invalid ID!" 

    parts = student_id.split("-")
    if len(parts) != 4:
        return False, "Invalid ID format!"

    uni_code, dept_part, code_part, number_part = parts

    if not len(code_part) == 2 or not code_part == "01":
        return False, "Invalid ID code part!"

    if not number_part.isdigit() or len(number_part) != 4:
        return False, "Invalid ID number part!"
    return True, "Valid ID"  

def validate_course_code(course_code):
    if not course_code or len(course_code) != 6:
        return False, "Invalid course code length!"
    prefix = course_code[:3]
    number = course_code[3:]

    if not prefix.isalpha() or not prefix.isupper():
        return False, "Invalid course code prefix!"
    if not number.isdigit():
        return False, "Invalid course code number!"
    return True, "Valid course code"  

def parse_date(date_str):
    try:
        day, month, year = map(int, date_str.split("-"))
        return (day, month, year)
    except:
        return None
    
def date_to_string(day, month, year):
    return f"{day:02d}-{month:02d}-{year:04d}"
    
def is_date_before(date1, date2):
    d1, m1, y1 = date1
    d2, m2, y2 = date2
    if y1 != y2:
        return y1 < y2
    if m1 != m2:
        return m1 < m2
    return d1 < d2

class Courses:
    def __init__(self, course_code, course_name, lecturer="", fee=0):
        self.course_code = course_code
        self.course_name = course_name
        self.lecturer = lecturer
        self.current_enrollment = []
        self.schedule = []
        self.fee = fee
        self.credits = 0  
        self.max_capacity = 30  

        valid, message = self._validate()  
        if not valid:
            raise ValueError(f"Invalid course data for {self.course_code}! {message}")
    
    def _validate(self):
        valid_code, msg_code = validate_course_code(self.course_code)  
        if not valid_code:
            return False, msg_code
        
        if not self.course_name or len(self.course_name.strip()) == 0:
            return False, "Invalid course name!"
        return True, "Valid course"
    
    def assign_lecturer(self, lecturer):
        self.lecturer = lecturer
        return f"Lecturer {lecturer} assigned to course {self.course_code}."
        
    def add_schedule(self, day, start_time, end_time, venue):
        try:
            start_h, start_m = map(int, start_time.split(":"))
            end_h, end_m = map(int, end_time.split(":"))

            if not (0 <= start_h < 24 and 0 <= start_m < 60):
                raise ValueError("Invalid start time format!")
            if not (0 <= end_h < 24 and 0 <= end_m < 60):
                raise ValueError("Invalid end time format!")

            start_total_minutes = start_h * 60 + start_m 
            end_total_minutes = end_h * 60 + end_m

            if start_total_minutes >= end_total_minutes:
                raise ValueError("End time must be after start time!")
            
            if (end_total_minutes - start_total_minutes) > 180:
                return False, "Class duration exceeds 3 hours!"
        except Exception as e:
            return False, f"Schedule error: {e}"
        
        self.schedule.append((day, start_time, end_time, venue))
        return True, "Schedule added successfully"
    
    def _calculate_fee(self):
        base_fee = 50000
        if self.course_code.startswith("CS"):
            return base_fee + 20000
        elif self.course_code.startswith("SE"):
            return base_fee + 25000
        else:
            return base_fee
    
    def has_schedule_conflict(self, other_course):
        for day1, start1, end1, venue1 in self.schedule:
            for day2, start2, end2, venue2 in other_course.schedule:
                if day1 == day2:
                    start1_h, start1_m = map(int, start1.split(":"))
                    end1_h, end1_m = map(int, end1.split(":"))
                    start2_h, start2_m = map(int, start2.split(":"))
                    end2_h, end2_m = map(int, end2.split(":"))

                    start1_total = start1_h * 60 + start1_m
                    end1_total = end1_h * 60 + end1_m
                    start2_total = start2_h * 60 + start2_m
                    end2_total = end2_h * 60 + end2_m

                    if (start1_total < end2_total and start2_total < end1_total):
                        return True
        return False
    
    def enroll_student(self, student_id):
        if student_id in self.current_enrollment:
            return False, f"Student {student_id} is already enrolled in {self.course_code}."
        if len(self.current_enrollment) >= self.max_capacity:
            return False, f"Course {self.course_code} is full."
        self.current_enrollment.append(student_id)
        return True, f"Student {student_id} enrolled in course {self.course_code}."
    
    def get_available_seats(self): 
        return self.max_capacity - len(self.current_enrollment)
    
    def store_course_data(self, filename):
        try:
            with open("course_data.txt", "w") as file:
                file.write(f"Course Code: {self.course_code}\n")
                file.write(f"Course Name: {self.course_name}\n")
                file.write(f"Lecturer: {self.lecturer}\n")
                file.write(f"Fee: {self.fee}\n")
                file.write(f"Credits: {self.credits}\n")
                file.write(f"Max Capacity: {self.max_capacity}\n")
                file.write(f"Current Enrollment: {len(self.current_enrollment)}\n")
                file.write("Schedule:\n")
                for day, start_time, end_time, venue in self.schedule:
                    file.write(f"  {day}: {start_time} - {end_time} at {venue}\n")
                file.write("Enrolled Students:\n")
                for student_id in self.current_enrollment:
                    file.write(f"  {student_id}\n")
            return f"Course data for {self.course_code} stored in {filename}."
        except Exception as e:
            return f"Error storing course data: {e}"

class Student:
    def __init__(self, student_id, name, email, admission_date, program="", admission_year=2024):  
        self.student_id = student_id
        self.name = name
        self.email = email
        self.enrolled_courses = []
        self.fees_paid = 0.0
        self.balance = 0.0
        self.payment_history = []
        self.admission_date = admission_date
        self.total_credits = 0
        self.program = program  
        self.admission_year = admission_year  
        self.gpa = 0.0  
        self.tuition_balance = 0.0
        self.completed_courses = []  

        valid, message = self.validate()
        if not valid:
            raise ValueError(f"Invalid student data for {self.student_id}! {message}")
    
    def validate(self):
        valid_id, msg_id = validate_student_id(self.student_id)  
        if not valid_id:
            return False, msg_id
        valid_email, msg_email = validate_student_email(self.email) 
        if not valid_email:
            return False, msg_email
        return True, "Valid student data!"
    
    def enroll_in_course(self, course):
        success, message = course.enroll_student(self.student_id)  
        if success:
            self.enrolled_courses.append(course.course_code)
            return True, f"Student {self.student_id} successfully enrolled in {course.course_code}."
        return False, f"Enrollment failed for student {self.student_id} in {course.course_code}: {message}"

    def list_enrolled_courses(self):
        return self.enrolled_courses
    
    def pay_fees(self, amount, date_str):
        if amount <= 0:
            return False, "Payment amount must be positive."
        self.fees_paid += amount
        self.balance -= amount
        self.tuition_balance -= amount  
        self.payment_history.append((amount, date_str))
        return True, f"Student {self.student_id} paid {amount} on {date_str}."
    
    def calculate_balance(self, total_fees):
        self.balance = total_fees - self.fees_paid
        return self.balance
    
    def get_current_semester_credits(self):
        total = 0
        for course_code in self.enrolled_courses:
            if course_code.startswith("CS") or course_code.startswith("SE"):
                total += 3
            else:
                total += 2
        return total
    
    def calculate_gpa(self):  
        grade_points = {
            "A": 4.0, "B": 3.0,
            "C": 2.0, "D": 1.0, "F": 0.0
        }
        
        total_points = 0
        total_credits = 0
        
        for course_code, grade in self.completed_courses:
            if grade in grade_points:
                credits = 3 if course_code.startswith(("CS", "SE")) else 2
                total_points += grade_points[grade] * credits
                total_credits += credits
        
        self.gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
        return self.gpa
    
    def add_tuition_fee(self, amount):  
        self.tuition_balance += amount
        return self.tuition_balance
    
    def store_student_data(self, filename):
        try:
            with open("student_data.txt", "w") as file:
                file.write(f"Student ID: {self.student_id}\n")
                file.write(f"Name: {self.name}\n")
                file.write(f"Email: {self.email}\n")
                file.write(f"Program: {self.program}\n")
                file.write(f"Admission Year: {self.admission_year}\n")
                file.write(f"GPA: {self.gpa}\n")
                file.write(f"Tuition Balance: ${self.tuition_balance:.2f}\n")
                file.write("Enrolled Courses:\n")
                for course_code in self.enrolled_courses:
                    file.write(f"  {course_code}\n")
                file.write("Completed Courses:\n")
                for course_code, grade in self.completed_courses:
                    file.write(f"  {course_code}: {grade}\n")
                file.write(f"Fees Paid: {self.fees_paid}\n")
                file.write(f"Balance: {self.balance}\n")
                file.write("Payment History:\n")
                for amount, date_str in self.payment_history:
                    file.write(f"  {amount} on {date_str}\n")
            return f"Student data for {self.student_id} stored in {filename}."
        except Exception as e:
            return f"Error storing student data: {e}"

class Enrollment:
    def __init__(self, student_id, course_code, semester):
        self.enrollment_id = self._generate_id()
        self.student_id = student_id
        self.course_code = course_code
        self.semester = semester
        self.enrollment_date = self._get_current_date()
        self.status = "ACTIVE"
        self.grade = None
        self.attendance_record = 100.0
        self.course_credits = 0
        self.exam_score = None
        self.final_grade_value = None  
        self.assignments = []

    def _generate_id(self):
        import time
        return f"ENR-{int(time.time())}"
    
    def _get_current_date(self):
        from datetime import datetime
        return datetime.now().strftime("%d-%m-%Y")
    
    def is_passing(self):
        if not self.grade:
            return False
        
        passing_grades = ['A', 'B', 'C', 'D']
        return self.grade in passing_grades
    
    def calculate_final_grade(self, assignments_weight=0.3, exam_weight=0.7):  
        if not self.assignments or self.exam_score is None:
            return None
        
        if self.assignments:
            avg_assignment_score = sum(self.assignments) / len(self.assignments)
        else:
            avg_assignment_score = 0

        final_score = (avg_assignment_score * assignments_weight) + (self.exam_score * exam_weight)
        
        if final_score >= 70:
            self.final_grade_value = 'A'
        elif final_score >= 60:
            self.final_grade_value = 'B'
        elif final_score >= 50:
            self.final_grade_value = 'C'
        elif final_score >= 40:
            self.final_grade_value = 'D'
        else:
            self.final_grade_value = 'F'
        
        return self.final_grade_value
        
    def add_assignment_score(self, score):
        if 0 <= score <= 100:
            self.assignments.append(score)
            return True, f"Added assignment score {score} for enrollment {self.enrollment_id}."
        else:
            return False, f"Invalid score {score}. Must be between 0 and 100."
    
    def withdraw(self, withdraw_date=None):
        if self.status != "ACTIVE":
            return False, f"Enrollment {self.enrollment_id} is not active."
        self.status = "WITHDRAWN"
        return True, f"Enrollment {self.enrollment_id} successfully withdrawn."

    def store_enrollment_data(self, filename):
        try:
            with open("enrollment_data.txt", "w") as file:
                file.write(f"Enrollment ID: {self.enrollment_id}\n")
                file.write(f"Student ID: {self.student_id}\n")
                file.write(f"Course Code: {self.course_code}\n")
                file.write(f"Semester: {self.semester}\n")
                file.write(f"Enrollment Date: {self.enrollment_date}\n")
                file.write(f"Status: {self.status}\n")
                file.write(f"Grade: {self.grade}\n")
                file.write(f"Attendance Record: {self.attendance_record}\n")
                file.write(f"Course Credits: {self.course_credits}\n")
                file.write(f"Exam Score: {self.exam_score}\n")
                file.write(f"Final Grade: {self.final_grade_value}\n")
                file.write("Assignments Scores:\n")
                for score in self.assignments:
                    file.write(f"  {score}\n")
            return f"Enrollment data for {self.enrollment_id} stored in {filename}."
        except Exception as e:
            return f"Error storing enrollment data: {e}"

class Assets:
    def __init__(self, asset_id, name, type, location):
        self.asset_id = asset_id
        self.name = name
        self.type = type
        self.location = location
        self.status = "AVAILABLE"
        self.bookings = []  
        self.maintenance_records = []
        self.deposit_amount = 0.0

    def is_available(self, start_time, end_time):
        if self.status in ["MAINTENANCE", "UNAVAILABLE"]:
            return False

        for booking in self.bookings:  
            if booking['status'] in ["ACTIVE", "ONGOING"]:
                if not (end_time <= booking['start_time'] or start_time >= booking['end_time']):
                    return False

        for maintenance in self.maintenance_records:
            if not (end_time <= maintenance['start_time'] or start_time >= maintenance['end_time']):
                return False
        return True

    def book_asset(self, user_id, start_time, end_time):
        if not self.is_available(start_time, end_time):  
            return False, f"Asset {self.asset_id} is not available from {start_time} to {end_time}."

        booking_record = {
            'user_id': user_id,
            'start_time': start_time,
            'end_time': end_time,
            'status': "ACTIVE"
        }
        self.bookings.append(booking_record)  
        return True, f"Asset {self.asset_id} booked by user {user_id} from {start_time} to {end_time}."
    
    def check_in(self, booking_id):
        for booking in self.bookings:  
            if booking['user_id'] == booking_id and booking['status'] == "ACTIVE":
                booking['status'] = "ONGOING"
                return True, f"User {booking_id} checked in to asset {self.asset_id}."
        return False, f"No active booking found for user {booking_id} on asset {self.asset_id}."
    
    def check_out(self, booking_id, condition="GOOD"):
        for booking in self.bookings:  
            if booking['user_id'] == booking_id and booking['status'] == "ONGOING":
                booking['status'] = "COMPLETED"
                booking['condition'] = condition
                booking['return_time'] = self._get_current_datetime()

                has_upcoming = False
                current_time = self._get_current_datetime()

                for b in self.bookings:
                    if b['status'] == "ACTIVE" and b['start_time'] > current_time:
                        has_upcoming = True
                        break

                self.status = "AVAILABLE" if not has_upcoming else "BOOKED"
                return True, f"User {booking_id} checked out from asset {self.asset_id}."
        return False, f"No ongoing booking found for user {booking_id} on asset {self.asset_id}."
    
    def _get_current_datetime(self):
        from datetime import datetime
        return datetime.now().strftime("%d-%m-%Y %H:%M")
    
    def calculate_booking_fee(self, start_time, end_time, rate_per_hour):
        from datetime import datetime

        fmt = "%d-%m-%Y %H:%M"
        start_dt = datetime.strptime(start_time, fmt)
        end_dt = datetime.strptime(end_time, fmt)

        duration = end_dt - start_dt
        hours = duration.total_seconds() / 3600
        fee = hours * rate_per_hour
        return fee
    
    def add_maintenance_record(self, start_time, end_time, description):
        maintenance_record = {
            'start_time': start_time,
            'end_time': end_time,
            'description': description
        }
        self.maintenance_records.append(maintenance_record)
        self.status = "MAINTENANCE"
        return True, f"Added maintenance record for asset {self.asset_id} from {start_time} to {end_time}."
    
    def update_asset_status(self, new_status):
        valid_statuses = ["AVAILABLE", "BOOKED", "MAINTENANCE", "UNAVAILABLE"]
        if new_status in valid_statuses:
            self.status = new_status
            return True, f"Asset {self.asset_id} status updated to {new_status}."
        else:
            return False, f"Invalid status: {new_status}."
        
    def store_asset_data(self, filename):
        try:
            with open("asset_data.txt", "w") as file:
                file.write(f"Asset ID: {self.asset_id}\n")
                file.write(f"Name: {self.name}\n")
                file.write(f"Type: {self.type}\n")
                file.write(f"Location: {self.location}\n")
                file.write(f"Status: {self.status}\n")
                file.write(f"Deposit Amount: {self.deposit_amount}\n")
                file.write("Bookings:\n")
                for booking in self.bookings: 
                    file.write(f"  User ID: {booking['user_id']}, Start: {booking['start_time']}, End: {booking['end_time']}, Status: {booking['status']}\n")
                file.write("Maintenance Records:\n")
                for maintenance in self.maintenance_records:
                    file.write(f"  Start: {maintenance['start_time']}, End: {maintenance['end_time']}, Description: {maintenance['description']}\n")
            return f"Asset data for {self.asset_id} stored in {filename}."
        except Exception as e:
            return f"Failed to store asset data for {self.asset_id} in {filename}. Error: {e}"

class EnrollmentServices:
    def __init__(self, course_catalog, student_records):
        self.course_catalog = course_catalog
        self.student_records = student_records

    def enroll_student(self, student_id, course_code, semester):
        if student_id not in self.student_records:
            return None, f"Student {student_id} not found."
        if course_code not in self.course_catalog:
            return None, f"Course {course_code} not found."
        
        student = self.student_records[student_id]
        course = self.course_catalog[course_code]

        success, message = student.enroll_in_course(course)  
        if success:
            enrollment = Enrollment(student_id, course_code, semester)
            return enrollment, f"Student {student_id} enrolled in course {course_code} for semester {semester}."
        else:
            return None, message
    
    def withdraw_enrollment(self, enrollment):
        success, message = enrollment.withdraw()  
        if success:
            student = self.student_records.get(enrollment.student_id)
            course = self.course_catalog.get(enrollment.course_code)

            if student and course:
                if enrollment.course_code in student.enrolled_courses:
                    student.enrolled_courses.remove(enrollment.course_code)
                if enrollment.student_id in course.current_enrollment:
                    course.current_enrollment.remove(enrollment.student_id)
            return True, f"Enrollment {enrollment.enrollment_id} successfully withdrawn."
        return False, message
    
    def get_student_schedule(self, student_id, semester):
        student = self.student_records.get(student_id)
        if not student:
            return None, f"Student {student_id} not found."
        
        schedule = []
        for enrolled_course_code in student.enrolled_courses:
            course = self.course_catalog.get(enrolled_course_code)
            if course:
                for day, start_time, end_time, venue in course.schedule:
                    schedule.append(
                        {
                            "course_code": course.course_code,
                            "course_name": course.course_name,
                            "day": day,
                            "start_time": start_time,
                            "end_time": end_time,
                            "venue": venue,
                            "lecturer": course.lecturer
                        }
                    )
        
        day_order = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
        schedule.sort(key=lambda x: (day_order.get(x['day'], 8), x['start_time']))
        return schedule, "Schedule retrieved successfully"
    
    def store_schedule(self, student_id, semester):
        student = self.student_records.get(student_id)
        if not student:
            return None, f"Student {student_id} not found."
        
        schedule, message = self.get_student_schedule(student_id, semester)
        try:
            with open("schedule_data.txt", "w") as file:
                file.write(f"Schedule for Student ID: {student_id}, Semester: {semester}\n")
                for entry in schedule:
                    file.write(f"{entry['day']}: {entry['course_code']} - {entry['course_name']} from {entry['start_time']} to {entry['end_time']} at {entry['venue']} (Lecturer: {entry['lecturer']})\n")
            return f"Schedule data for student {student_id} stored in schedule_data.txt."
        except Exception as e:
            return f"Error storing schedule data: {e}"
    
    def store_enrollment_data(self, enrollment, filename):
        return enrollment.store_enrollment_data("enrollment_data.txt")  
    
class GradingService:
    def __init__(self, enrollment_records):
        self.enrollment_records = enrollment_records

    def assign_grade(self, enrollment_id, grade):
        enrollment = self.enrollment_records.get(enrollment_id)
        if not enrollment:
            return False, f"Enrollment {enrollment_id} not found."
        enrollment.grade = grade
        return True, f"Assigned grade {grade} to enrollment {enrollment_id}."

    def calculate_final_grade(self, enrollment_id, assignments_weight=0.3, exam_weight=0.7):
        enrollment = self.enrollment_records.get(enrollment_id)
        if not enrollment:
            return None, f"Enrollment {enrollment_id} not found."
        final_grade = enrollment.calculate_final_grade(assignments_weight, exam_weight)
        enrollment.final_grade_value = final_grade
        return final_grade, f"Final grade for enrollment {enrollment_id} is {final_grade}."

    def store_enrollment_data(self, enrollment, filename):
        return enrollment.store_enrollment_data("enrollment_data.txt")

class FinancialServices:
    def __init__(self, student_records):
        self.student_records = student_records

    def process_payment(self, student_id, amount, date_str):
        student = self.student_records.get(student_id)
        if not student:
            return False, f"Student {student_id} not found."
        return student.pay_fees(amount, date_str)

    def calculate_student_balance(self, student_id, total_fees):
        student = self.student_records.get(student_id)
        if not student:
            return None, f"Student {student_id} not found."
        balance = student.calculate_balance(total_fees)
        return balance, f"Student {student_id} has a balance of {balance}."
    
    def store_financial_data(self, student, filename):
        return student.store_student_data("student_data.txt")  

class CampusManagementSystem:
    def __init__(self):
        self.course_catalog = {}
        self.student_records = {}
        self.enrollment_records = {}
        self.asset_records = {}
        self.enrollment_service = EnrollmentServices(self.course_catalog, self.student_records)
        self.grading_service = GradingService(self.enrollment_records)
        self.financial_service = FinancialServices(self.student_records)

    def add_course(self, course_data):  
        try:
           
            course = Courses(
                course_code=course_data["code"],
                course_name=course_data["title"],
                lecturer=course_data.get("instructor", ""),
                fee=course_data.get("fee", 0)
            )
            course.credits = course_data.get("credits", 3)
            course.max_capacity = course_data.get("max_capacity", 30)
            
            if course.course_code in self.course_catalog:
                return False, f"Course {course.course_code} already exists in catalog."
            
            self.course_catalog[course.course_code] = course
            return True, f"Course {course.course_code} added successfully."
        except Exception as e:
            return False, f"Error adding course: {e}"
    
    def add_student(self, student_data):  
        try:
            student = Student(
                student_id=student_data["student_id"],
                name=student_data["name"],
                email=student_data["email"],
                admission_date=f"01-09-{student_data['admission_year']}",
                program=student_data.get("program", ""),
                admission_year=student_data.get("admission_year", 2024)
            )
            
            if student.student_id in self.student_records:
                return False, f"Student {student.student_id} already exists in records."
            
            self.student_records[student.student_id] = student
            return True, f"Student {student.student_id} added successfully."
        except Exception as e:
            return False, f"Error adding student: {e}"

    def enroll_student_in_course(self, student_id, course_code, semester):
        enrollment, message = self.enrollment_service.enroll_student(student_id, course_code, semester)
        if enrollment:
            enrollment_key = f"{student_id}_{course_code}_{semester}"
            self.enrollment_records[enrollment_key] = enrollment
            return True, f"Enrollment successful. ID: {enrollment.enrollment_id}"
        return False, message

    def assign_grade_to_enrollment(self, enrollment_id, grade):
        return self.grading_service.assign_grade(enrollment_id, grade)

    def process_student_payment(self, student_id, amount, date_str):
        return self.financial_service.process_payment(student_id, amount, date_str)

    def add_asset(self, asset):
        try:
            if asset.asset_id in self.asset_records:
                return False, f"Asset {asset.asset_id} already exists in records."
            self.asset_records[asset.asset_id] = asset
            return True, f"Asset {asset.asset_id} added successfully."
        except Exception as e:
            return False, f"Error adding asset: {e}"

    def process_grade_submission(self, lecturer_id, course_code, grade_data):
        if course_code not in self.course_catalog:
            return False, f"Course {course_code} not found."
        course = self.course_catalog[course_code]
        if course.lecturer != lecturer_id:
            return False, f"Lecturer {lecturer_id} is not assigned to course {course_code}."

        results = []
        for grade_item in grade_data:  
            student_id = grade_item["student_id"]
            grade = grade_item["grade"]
            
            enrollment_key = f"{student_id}_{course_code}_2024A"   
            enrollment = self.enrollment_records.get(enrollment_key)
            
            if enrollment:
                self.grading_service.assign_grade(enrollment.enrollment_id, grade)
                final_grade, _ = self.grading_service.calculate_final_grade(enrollment.enrollment_id)
                
                
                student = self.student_records.get(student_id)
                if student:
                    student.completed_courses.append((course_code, final_grade))
                    student.calculate_gpa()  

                results.append((student_id, final_grade))
            else:
                return False, f"Enrollment for student {student_id} in course {course_code} not found."
        
        return results, "Grades processed successfully"

    def book_campus_asset(self, asset_id, user_id, start_time, end_time):
        asset = self.asset_records.get(asset_id)
        if not asset:
            return False, f"Asset {asset_id} not found."
        return asset.book_asset(user_id, start_time, end_time)

    def generate_student_report(self, student_id):
        student = self.student_records.get(student_id)
        if not student:
            return False, f"Student {student_id} not found."

        report = {
            "student_id": student.student_id,  
            "name": student.name,
            "email": student.email,
            "enrolled_courses": student.enrolled_courses,
            "fees_paid": student.fees_paid,
            "balance": student.balance,
            "payment_history": student.payment_history,
            "gpa": student.gpa,
            "tuition_balance": student.tuition_balance,
            "completed_courses": student.completed_courses
        }
        return True, report

    def generate_student_transcript(self, student_id):  
        student = self.student_records.get(student_id)
        if not student:
            return None
        
        transcript = {
            "name": student.name,
            "student_id": student.student_id,
            "program": student.program,
            "admission_year": student.admission_year,
            "gpa": student.gpa,
            "total_credits": student.total_credits,
            "courses": student.completed_courses
        }
        return transcript

    def generate_course_report(self, course_code):
        course = self.course_catalog.get(course_code)
        if not course:
            return False, f"Course {course_code} not found."

        report = {
            "course_code": course.course_code,  
            "course_name": course.course_name,
            "lecturer": course.lecturer,
            "current_enrollment": course.current_enrollment,
            "schedule": course.schedule,
            "fee": course.fee,
            "credits": course.credits,
            "max_capacity": course.max_capacity,
            "available_seats": course.get_available_seats()
        }
        return True, report

    def store_system_data(self, filename):
        try:
            with open("system_data.txt", "w") as file:
                file.write("Campus Management System Data Overview\n")
                file.write(f"Total Courses: {len(self.course_catalog)}\n")
                file.write(f"Total Students: {len(self.student_records)}\n")
                file.write(f"Total Enrollments: {len(self.enrollment_records)}\n")
                file.write(f"Total Assets: {len(self.asset_records)}\n")
        except Exception as e:
            print(f"Error storing system data: {e}")

    def store_system_report(self, filename):
        try:
            with open(self,"system_report.txt", "w") as file:
                file.write("Campus Management System Report\n")
                file.write(f"Total Courses: {len(self.course_catalog)}\n")
                file.write(f"Total Students: {len(self.student_records)}\n")
                file.write(f"Total Enrollments: {len(self.enrollment_records)}\n")
                file.write(f"Total Assets: {len(self.asset_records)}\n")
        except Exception as e:
            print(f"Error storing system report: {e}")        

    def store_course_report(self, course_code, filename):
        course = self.course_catalog.get(course_code)
        if not course:
            return f"Course {course_code} not found."

        try:
            with open("course_report.txt", "w") as file:
                file.write(f"Course Report for {course.course_code}\n")
                file.write(f"Course Name: {course.course_name}\n")
                file.write(f"Lecturer: {course.lecturer}\n")
                file.write(f"Current Enrollment: {len(course.current_enrollment)}\n")
                file.write("Schedule:\n")
                for day, start_time, end_time, venue in course.schedule:
                    file.write(f"  {day}: {start_time} - {end_time} at {venue}\n")
                file.write(f"Fee: {course.fee}\n")
                file.write(f"Credits: {course.credits}\n")
                file.write(f"Max Capacity: {course.max_capacity}\n")
                file.write(f"Available Seats: {course.get_available_seats()}\n")
            return f"Course report for {course.course_code} stored in {filename}."
        except Exception as e:
            return f"Error storing course report: {e}"
    def store_student_report(self, student_id, filename):
        student = self.student_records.get(student_id)
        if not student:
            return f"Student {student_id} not found."

        try:
            with open("student_report.txt", "w") as file:
                file.write(f"Student Report for {student.student_id}\n")
                file.write(f"Name: {student.name}\n")
                file.write(f"Email: {student.email}\n")
                file.write(f"Program: {student.program}\n")
                file.write(f"Admission Year: {student.admission_year}\n")
                file.write(f"GPA: {student.gpa}\n")
                file.write(f"Tuition Balance: ${student.tuition_balance:.2f}\n")
                file.write("Enrolled Courses:\n")
                for course_code in student.enrolled_courses:
                    file.write(f"  {course_code}\n")
                file.write("Completed Courses:\n")
                for course_code, grade in student.completed_courses:
                    file.write(f"  {course_code}: {grade}\n")
                file.write(f"Fees Paid: {student.fees_paid}\n")
                file.write(f"Balance: {student.balance}\n")
                file.write("Payment History:\n")
                for amount, date_str in student.payment_history:
                    file.write(f"  {amount} on {date_str}\n")
            return f"Student report for {student.student_id} stored in {filename}."
        except Exception as e:
            return f"Error storing student report: {e}"

    def store_student_transcript(self, student_id, filename):
        student = self.student_records.get(student_id)
        if not student:
            return f"Student {student_id} not found."

        try:
            with open("student_transcript.txt", "w") as file:
                file.write(f"Transcript for {student.name} (ID: {student.student_id})\n")
                file.write(f"Program: {student.program}\n")
                file.write(f"Admission Year: {student.admission_year}\n")
                file.write(f"GPA: {student.gpa}\n")
                file.write(f"Total Credits: {student.total_credits}\n")
                file.write("Completed Courses:\n")
                for course_code, grade in student.completed_courses:
                    file.write(f"  {course_code}: {grade}\n")
            return f"Student transcript for {student.student_id} stored in {filename}."
        except Exception as e:
            return f"Error storing student transcript: {e}"
                        
    def get_system_report(self):  
        return self.store_system_report("system_report.txt")
    
    def get_system_data(self):  
        return self.store_system_data("system_data.txt")


def demonstrate_system():
    """Demonstrate the campus management system in action"""
    print("=" * 60)
    print("PCOS CORE CAMPUS LOGIC DEMONSTRATION")
    print("=" * 60)
    
    # Initialize system
    cms = CampusManagementSystem()
    
    # Add courses - USE 6-CHARACTER COURSE CODES
    print("\n1. ADDING COURSES:")
    courses_to_add = [
        {
            "code": "CSE101",  # FIXED: 6 characters - "CSE" + "101"
            "title": "Introduction to Computer Science",
            "credits": 3,
            "instructor": "DR_SMITH",
            "max_capacity": 25,
            "fee": 70000
        },
        {
            "code": "MTH201",  # FIXED: 6 characters - "MTH" + "201"
            "title": "Calculus I",
            "credits": 4,
            "instructor": "DR_JOHNSON",
            "max_capacity": 30,
            "fee": 50000
        },
        {
            "code": "CSE201",  # FIXED: 6 characters - "CSE" + "201"
            "title": "Data Structures",
            "credits": 3,
            "instructor": "DR_SMITH",
            "max_capacity": 20,
            "fee": 75000
        }
    ]
    
    for course_data in courses_to_add:
        success, message = cms.add_course(course_data)
        print(f"  {message}")
        
        # Add schedule to CSE101
        if course_data["code"] == "CSE101":
            cse101 = cms.course_catalog["CSE101"]
            success, msg = cse101.add_schedule("Mon", "10:00", "11:30", "ROOM_101")
            if success:
                print(f"  Schedule added to CSE101")
            cse101.add_schedule("Wed", "10:00", "11:30", "ROOM_101")
    
    # Add students
    print("\n2. ADDING STUDENTS:")
    students_to_add = [
        {
            "student_id": "PCOS-01-01-0001",
            "name": "Alice Johnson",
            "email": "alice@picos.edu",
            "program": "Computer Science",
            "admission_year": 2024
        },
        {
            "student_id": "PCOS-01-01-0002",
            "name": "Bob Williams",
            "email": "bob@picos.edu",
            "program": "Computer Science",
            "admission_year": 2024
        }
    ]
    
    for student_data in students_to_add:
        success, message = cms.add_student(student_data)
        print(f"  {message}")
    
    # Enroll students
    print("\n3. ENROLLING STUDENTS:")
    
    # Alice enrolls in CSE101
    success, message = cms.enroll_student_in_course("PCOS-01-01-0001", "CSE101", "2024A")
    print(f"  Alice enrolls in CSE101: {message}")
    
    # Bob enrolls in CSE101
    success, message = cms.enroll_student_in_course("PCOS-01-01-0002", "CSE101", "2024A")
    print(f"  Bob enrolls in CSE101: {message}")
    
    # Process grades for CSE101
    print("\n4. PROCESSING GRADES:")
    grade_data = [
        {"student_id": "PCOS-01-01-0001", "grade": "A"},
        {"student_id": "PCOS-01-01-0002", "grade": "B+"}
    ]
    
    results, message = cms.process_grade_submission("DR_SMITH", "CSE101", grade_data)
    if results:
        print(f"  Grades submitted successfully")
        for student_id, grade in results:
            print(f"    {student_id}: {grade}")
    
    # Generate transcript
    print("\n5. GENERATING TRANSCRIPT:")
    transcript = cms.generate_student_transcript("PCOS-01-01-0001")
    if transcript:
        print(f"  Transcript for {transcript['name']}:")
        print(f"    GPA: {transcript['gpa']}")
        print(f"    Program: {transcript['program']}")
        print(f"    Courses Completed: {len(transcript['courses'])}")
        for course, grade in transcript['courses']:
            print(f"      {course}: {grade}")
    
    # System report
    print("\n6. SYSTEM REPORT:")
    report = cms.store_system_report()
    
    print(report)
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    
    return cms
# ==================== MAIN EXECUTION ====================

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Run demonstration
    cms = demonstrate_system()
    
    # Run business rule tests
    run_business_rule_tests()
    
    # Example of using the system programmatically
    print("\n" + "=" * 60)
    print("QUICK SYSTEM ACCESS EXAMPLE")
    print("=" * 60)
    
    # Check a specific student
    if "PCOS-01-01-0001" in cms.student_records:
        student = cms.student_records["PCOS-01-01-0001"]
        print(f"\nStudent: {student.name}")
        print(f"Email: {student.email}")
        print(f"Program: {student.program}")
        print(f"GPA: {student.gpa}")
        print(f"Tuition Balance: ${student.tuition_balance:.2f}")
        print(f"Current Enrollments: {len(student.enrolled_courses)}")
    
    # Check a specific course
    if "CSE101" in cms.course_catalog:
        course = cms.course_catalog["CSE101"]
        print(f"\nCourse: {course.course_code} - {course.course_name}")
        print(f"Instructor: {course.lecturer}")
        print(f"Credits: {course.credits}")
        print(f"Enrollment: {len(course.current_enrollment)}/{course.max_capacity}")
        print(f"Available Seats: {course.get_available_seats()}")
        print(f"Course Fee: ${course.fee:.2f}")