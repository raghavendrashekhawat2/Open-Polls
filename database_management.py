import sqlite3
conn = sqlite3.connect('Voting_database.db')
c = conn.cursor()


table_name = "poll_no" + str(2)
query = """select * from {}""".format(table_name)
c.execute(query)
row = c.fetchall()
print(row)
# # table_name = 'custom'
# valid_mails = ["raghavendrashekhawat1@gmail.com", "raghavendrashekhawat2@gmail.com", "raghavendrashekhawat3@gmail.com"]
#
# for mail in valid_mails:
#     print(mail)
#     query = """ INSERT INTO {}(emailid, option) VAlUES(:m, :o) """.format(table_name)
#     c.execute(query, {"m": mail, "o": 0})


# c.execute("""CREATE TABLE login_creds (
#                 userid INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username VARCHAR(30) NOT NULL,
#                 password TEXT NOT NULL
#                 ) """)
# c.execute("""INSERT INTO login_creds (username, password) VALUES( 'Cham', 'hamp')""")

# c.execute("""delete from user_data where userid == 1""")

# c.execute(""" SELECT * FROM poll_data""")
# c.execute(""" SELECT * FROM poll_filters""")
# c.execute(""" SELECT * FROM poll_results""")
# c.execute(""" DROP TABLE custom""")
# c.execute(""" DROP TABLE poll_filters""")
# c.execute(""" DROP TABLE poll_results""")
# c.execute("""CREATE TABLE poll_data (
#                 pollid INTEGER PRIMARY KEY AUTOINCREMENT,
#                 owner INTEGER NOT NULL,
#                 pollname VARCHAR(30) NOT NULL,
#                 quest VARCHAR(300) NOT NULL,
#                 op1 VARCHAR(50) NOT NULL,
#                 op2 VARCHAR(50) NOT NULL,
#                 op3 VARCHAR(50),
#                 op4 VARCHAR(50),
#                 op5 VARCHAR(50),
#                 op6 VARCHAR(50),
#                 op7 VARCHAR(50),
#                 op8 VARCHAR(50)
#                 ) """)
#
# c.execute("""CREATE TABLE poll_filters (
#                 pollid INTEGER PRIMARY KEY AUTOINCREMENT,
#                 start DATE NOT NULL,
#                 end DATE NOT NULL,
#                 public INTEGER,
#                 private INTEGER,
#                 no_of_options INTEGER,
#                 age INTEGER,
#                 gender VARCHAR(50),
#                 state VARCHAR(50)
#                 ) """)
#
# c.execute("""CREATE TABLE poll_results (
#                 pollid INTEGER PRIMARY KEY AUTOINCREMENT,
#                 op1 INTEGER,
#                 op2 INTEGER,
#                 op3 INTEGER,
#                 op4 INTEGER,
#                 op5 INTEGER,
#                 op6 INTEGER,
#                 op7 INTEGER,
#                 op8 INTEGER
#                 ) """)
conn.commit()
