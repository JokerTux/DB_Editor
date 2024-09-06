import sqlite3
import sys
import argparse
from werkzeug.security import generate_password_hash

def main():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    login = input('login : ')
    password = input('password : ')
    password = generate_password_hash(password)
    admin = input('if admin press 1; if moderator press 0 : ')
    active = False
    try:
        cur.execute("INSERT INTO user(username, password, admin, active) VALUES(?,?,?,?)",(login, password, admin, active))
        con.commit()
        print("done")
    except sqlite3.Error as e:
        print(e)	
    finally:
        con.close()

if __name__ == "__main__":
	main()			
