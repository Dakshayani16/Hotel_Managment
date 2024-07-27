import sqlite3

##table1 - customerid tableno total
try:
    con=sqlite3.connect('hotel.db')
    cur=con.cursor()
    query1="Create table if not exist table1(personid int AUTO_INCREMENT,tableno int,total int)"
    cur.execute(query1)
    query1="Create table if not exist table2(tableno int,item varchar(30),Quantity int,cost int)"
    cur.execute(query1)

except sqlite3.Error as e:
    print('Error')

##table2- order tableno- payement method item quantity cost
