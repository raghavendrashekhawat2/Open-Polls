import sqlite3
conn = sqlite3.connect('Voting_database.db')
c = conn.cursor()

# c.execute("""CREATE TABLE login_creds (
#                 userid INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username VARCHAR(30) NOT NULL,
#                 password TEXT NOT NULL
#                 ) """)
# c.execute("""INSERT INTO login_creds (username, password) VALUES( 'Cham', 'hamp')""")


c.execute("""delete from login_creds where userid == 1 AND userid == 2""")
conn.commit()
row = c.fetchall()

print(row)