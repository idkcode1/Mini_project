import sqlite3
import cv2
con = sqlite3.connect('Time5.db')
# con = sqlite3.connect(':memory:')
c = con.cursor()

# c.execute("""CREATE TABLE timestamp(
#             day text,
#             driver text,
#             time integer
#             )""")
#
# c.execute("""CREATE TABLE timestamp(day text,name text, time integer)""")
def insert_timestamp(n):
    con = sqlite3.connect('Time5.db')
    c = con.cursor()
    # with con:
    c.execute("INSERT INTO timestamp (day, name, time) VALUES (?,?,?)", (n.day, n.name, n.time))
    con.commit()
    # c.execute("SELECT * FROM timestamp")
    # print(c.fetchall())
    con.close()


c.execute("SELECT * FROM timestamp ")
# c.execute("SELECT * FROM timestamp ORDER BY time DESC")
# print(c.fetchall())
for i in range(300):
    print("\n")
    print(c.fetchone())
con.close()