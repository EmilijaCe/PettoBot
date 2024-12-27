import mysql.connector

def __init__(password, database):
    global con
    con = mysql.connector.connect(host = 'localhost', user = 'root', password = password, database = database)
    global mycursor
    mycursor = con.cursor()

def insert(tablename, items, values):
    line = "insert into " + tablename + " ("
    last = len(items) - 1
    for i in range(items):
        if i == last:
            line += items[i] + ") "
        else:
            line += items[i] + ", "
    line += "values ("
    for i in range(items):
        if i == last:
            line += "%s);"
        else:
            line += "%s, "
    mycursor.execute(line, values)
    con.commit()

def update(tablename, items, values, whereitem, wherevalue):
    line = "update " + tablename + " set "
    last = len(items) - 1
    for i in range(items):
        line += items[i] + " = " + values[i]
        if i != last:
            line += ", "
    line += " where " + whereitem + " = " + wherevalue + ";"
    mycursor.execute(line)
    con.commit()

def select(tablename, items, whereitem, wherevalue):
    line = "select "
    last = len(items) - 1
    for i in range(items):
        line += str(items[i])
        if i != last:
            line += ", "
    line += " from " + tablename + " where " + whereitem + " = " + wherevalue + ";"
    mycursor.execute(line)
    results = mycursor.fetchone()
    return results

def select(tablename, items):
    line = "select "
    last = len(items) - 1
    for i in range(items):
        line += str(items[i])
        if i != last:
            line += ", "
    line += " from " + tablename + ";"
    mycursor.execute(line)
    results = mycursor.fetchall()
    return results