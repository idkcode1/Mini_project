import sqlite3
con = sqlite3.connect('/home/raspberry/Desktop/test1/Time6.db')
# con = sqlite3.connect(':memory:')
c = con.cursor()
# c.execute("""CREATE TABLE timestt(
#                  day text,
#                  driver text,
#                  time integer
#                  )""")

def insert_timestamp(n):
    con = sqlite3.connect('/home/raspberry/Desktop/test1/Time6.db')
    c = con.cursor()
    # with con:
    c.execute("INSERT INTO timestt(day, driver, time) VALUES (?,?,?)", (n.day, n.driver, n.time))
    con.commit()
    # c.execute("SELECT * FROM timestamp")
    # print(c.fetchall())
    con.close()


c.execute("SELECT * FROM timestt ")
# c.execute("SELECT * FROM timestamp ORDER BY time DESC")

for i in range(10):
     print("\n")
     print(c.fetchone())
con.close()