import sqlite3
conn = sqlite3.connect('Voting_database.db')
c = conn.cursor()

# Table 1
# c.execute("""CREATE TABLE login_creds (
#                 userid INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username VARCHAR(30) NOT NULL,
#                 password TEXT NOT NULL
#                 ) """)

# Table 2

# c.execute("""CREATE TABLE user_data (
#                 userid INTEGER PRIMARY KEY,
#                 First_Name VARCHAR(30) NOT NULL,
#                 Last_Name VARCHAR(30) NOT NULL,
#                 Dob DATE NOT NULL,
#                 State VARCHAR(50) NOT NULL,
#                 Mob_Number TEXT NOT NULL,
#                 Gender VARCHAR(6) NOT NULL,
#                 Email text NOT NULL
#                 ) """)


