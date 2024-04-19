import sqlite3
import bcrypt
from functions import validate_email
from functions import hash


db = sqlite3.connect("register.db")
db.create_function('hash', 1, hash)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS reg(
            
            username VARCHAR(16) UNIQUE NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL
)""")



first_name = input("First name: ")
last_name = input("Last name: ")
while True:
    username = input("Username: ")
    usernamecheck = sql.execute(f"SELECT COUNT(*) FROM reg WHERE username = '{username}'")
    usernamecheck = int("".join(map(str, sql.fetchone())))
    if usernamecheck == 0:
        email = input("Email: ")   
        emailcheck = sql.execute(f"SELECT COUNT(*) FROM reg WHERE email = '{email}'")
        emailcheck = int("".join(map(str, sql.fetchone())))
        if emailcheck == 0:
            if validate_email(email):
                password1 = input("Password: ")
                password2 = input("Confirm password: ")
                if password1 == password2:
                    sql.execute("INSERT INTO reg VALUES(?, ?, ?, ?, hash(?))", (username, first_name, last_name, email, password1))
                    db.commit()
                    print("SUCCESS")
                    break
                else:
                    print("Shifreler eyni deyil! ")
            else:
                print("Email duzgun yazilmayib!")
        else:
            print("Email bazada mocuddur!")
    else:
        print("Username bazada movcuddur!")








def check_password(): ## shifrenin duzgunluyun yoxlamaq ucun
    username = input("Username: ")
    password = input("Password: ")
    sql.execute(f"SELECT * FROM reg WHERE username = '{username}'")
    user = sql.fetchone()
    if user:
        if bcrypt.checkpw(password.encode('-utf-8'), user[4]):
            return 'Success'
        else:
            return 'Wrong password'
    return "Username not found!"

# print(check_password())



