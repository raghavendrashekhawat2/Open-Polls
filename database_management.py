import datetime
import sqlite3
from helper import convert_date

conn = sqlite3.connect('Voting_database.db')
c = conn.cursor()

c.execute("SELECT pollid, end FROM poll_filters WHERE public == 1 ")
pub_polls = c.fetchall()
f_pub_polls = []
for i in pub_polls:
    print(i[0])
    c.execute(""" SELECT pollname FROM poll_data WHERE pollid == :p """, {"p": i[0]})
    name = c.fetchone()[0]
    print(name)
    t = [name, i[1]]
    f_pub_polls.append(t)


print(f_pub_polls)






# option = 0
# table_name = "poll_no4"
# email = "raghavendrashekhawat1@gmail.com"
# c.execute("""UPDATE {} SET option = :o""".format(table_name), {"o": option})
# c.execute(""" INSERT INTO poll_no5(emailid, option) VALUES('raghavendrashekhawat1@gmail.com', 0)""")
# poll_id = 2
# c.execute("""UPDATE {} SET option = :o WHERE emailid == :e""".format(table_name), {"o": option, "e": email})
# query = """SELECT * from {}""".format(table_name)
# c.execute(query)

# print()
# c.execute("SELECT * FROM login_creds ")
# rows = c.fetchall()
# for row in rows:
#     print(row)

# c.execute("""SELECT * FROM poll_results JOIN poll_data USING (pollid) WHERE pollid = :p """, {"p": 2})
#
# data = c.fetchone()
# print(data)
# c.execute("""SELECT no_of_options FROM poll_filters WHERE pollid = :p""", {"p" : 2})
# data = c.fetchone()
# print(data[0])

c.execute("""SELECT COUNT(userid) FROM login_creds""")
user_count = c.fetchone()[0]
print(user_count)
# c.execute("""SELECT email from user_data WHERE userid = :u """, {"u": 2})
# email = c.fetchone()[0]
# c.execute("""SELECT pollid from poll_filters WHERE private == 1""")
# poll_id = c.fetchall()
# print(poll_id, email)
#
#
# final_p = []
# final_options = []
# # Check if user has access to the poll if yes then add to final_p and final_options
# for idx in poll_id:
#     table_name = "poll_no" + str(idx[0])
#     c.execute("""SELECT option from {} where emailid == :o """.format(table_name), {"o": email})
#     option = c.fetchone()
#     if option is not None:
#         final_p.append(idx[0])
#         final_options.append(option[0])
#
# poll_name = []
# poll_dates = []
#
# for idx in final_p:
#     c.execute("""SELECT pollname from poll_data WHERE pollid == :p""", {"p": idx})
#     poll_name.append(c.fetchone())
#     c.execute("""SELECT start, end from poll_filters WHERE pollid == :p""", {"p": idx})
#     poll_dates.append(c.fetchone())
#
# final_data = []
#
# # Organize data into a single list
# # Check if poll has expired
# for i in range(len(final_p)):
#     data = [final_p[i], poll_name[i][0], convert_date(poll_dates[i][0]), convert_date(poll_dates[i][1]),
#             final_options[i]]
#     # Convert Starting data from yyyy/mm/dd to 4 April
#     if not compare_date(poll_dates[i][0]):
#         data.append(0)
#     else:
#         # Convert Ending data from yyyy/mm/dd to 4 April
#         data.append(1)
#     final_data.append(data)
# print(final_data)


# c.execute(""" UPDATE "user_data" SET "userid"='2', "First_Name"='Raghavendra', "Last_Name"='Shekhawat', "Dob"='1999-12-04', "State"='Rajasthan', "Mob_Number"='9027592291', "Gender"='Male', "Email"='raghavendrashekhawat1@gmail.com' WHERE "rowid" = 2 """)

#
# table_name = "poll_no" + str(10)
# query = """select * from {}""".format(table_name)
#
# email = "raghavendrashekhawat1@gmail.com"
# idx = 2
# table_name = "poll_no" + str(idx)
# query = """SELECT option from poll_no2 where email == :o """
#
# c.execute("""SELECT option from {} where emailid == :o """.format(table_name), {"o": email})
# row = c.fetchall()[0]
# print(row)
# print(query)
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
# c.execute("""INSERT INTO user_data (username, password) VALUES( 'Cham', 'hamp')""")

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
