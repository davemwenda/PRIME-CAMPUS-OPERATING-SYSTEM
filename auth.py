# login credentials

# usernames
student_email = "student25@dkut.ac.ke"
staff_email = "staff00@dkut.ac.ke"
admin_email = "admin01@dkut.ac.ke"

# passwords
student_password = "student1"
staff_password = "staff"
admin_password = "admin"

Attempt = 1


def student():

    print("#STUDENT ACCOUNT")
    # Password validation
    Attempt = 1
    while Attempt <= 3:
        password = input("Enter your password\n\t")
        if password == student_password:
            print("Successful login")
            Attempt = 4
            return

        else:
            print("incorrect password")

            Attempt += 1

            if Attempt == 4:
                print("too many attempts, please try again later")
                exit()
    # call student object


def staff():

    print("#STAFF ACCOUNT")
    # Password validation
    Attempt = 1
    while Attempt <= 3:
        password = input("Enter your password\n\t")
        if password == staff_password:
            print("Successful login")
            Attempt = 4

        else:
            print("incorrect password")

            Attempt += 1

            if Attempt == 4:
                print("too many attempts, please try again later")
                exit()
    # call staff object


def admin():

    print("#ADMIN ACCOUNT")
    # Password validation
    Attempt = 1
    while Attempt <= 3:
        password = input("Enter your password\n\t")
        if password == admin_password:
            print("Successful login")
            Attempt = 4

        else:
            print("incorrect password")

            Attempt += 1

            if Attempt == 4:
                print("too many attempts, please try again later")
                exit()
    # call admin object


print("login required")

# login/sign up


def login():

    attempt_1 = 0
    while attempt_1 <= 3:
        username1 = input("Enter your email\n\t")

        attempt_1 += 1

        if username1 == student_email:
            student()

        elif username1 == staff_email:
            staff()

        elif username1 == admin_email:
            admin()

        else:
            print("Please enter the correct email")
            if attempt_1 == 3:
                print("Too many attempts, please try again later")
                attempt_1 = 4
