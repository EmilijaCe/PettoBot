import mysql.connector


password = input("MYSQL password: ")

con = mysql.connector.connect(host = 'localhost', user = 'root', password = password, database = 'bots')
mycursor = con.cursor()

def insert(tablename, items, values):
    line = "insert into " + tablename + " ("
    last = len(items) - 1
    for i in range(len(items)):
        if i == last:
            line += items[i] + ") "
        else:
            line += items[i] + ", "
    line += "values ("
    for i in range(len(items)):
        if i == last:
            line += "%s);"
        else:
            line += "%s, "
    mycursor.execute(line, values)
    con.commit()

def update(tablename, items, values, whereitem, wherevalue):
    line = "update " + tablename + " set "
    last = len(items) - 1
    for i in range(len(items)):
        line += items[i] + " = " + str(values[i])
        if i != last:
            line += ", "
    line += " where " + whereitem + " = " + wherevalue + ";"
    mycursor.execute(line)
    con.commit()

def select(tablename, items, whereitem = None, wherevalue = None):
    line = "select "
    last = len(items) - 1
    for i in range(len(items)):
        line += str(items[i])
        if i != last:
            line += ", "
    line += " from " + tablename
    if whereitem != None:
        line += " where " + whereitem + " = " + str(wherevalue)
    line += ";"
    mycursor.execute(line)
    results = mycursor.fetchall()
    return results