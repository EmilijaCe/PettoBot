import mysql.connector
import main


#con = mysql.connector.connect(host = 'localhost', user = 'root', password = main.DBpassword, database = 'bots')
#con = mysql.connector.connect(host = 'pettobot-server.mysql.database.azure.com', user = 'efkabvewnb', password = password, database = 'pettobot-database')
con = mysql.connector.connect(user="efkabvewnb", password=main.DBpassword, host="pettobot-server.mysql.database.azure.com", port=3306, database="pettobot-database", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)
mycursor = con.cursor()

def insert(items, values):
    line = "insert into petbot ("
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

def update(items, values, whereitem, wherevalue):
    line = "update petbot set "
    last = len(items) - 1
    for i in range(len(items)):
        line += items[i] + " = " + str(values[i])
        if i != last:
            line += ", "
    line += " where " + whereitem + " = " + wherevalue + ";"
    mycursor.execute(line)
    con.commit()

def select(items, whereitem = None, wherevalue = None):
    line = "select "
    last = len(items) - 1
    for i in range(len(items)):
        line += str(items[i])
        if i != last:
            line += ", "
    line += " from petbot"
    if whereitem != None:
        line += " where " + whereitem + " = " + str(wherevalue)
    line += ";"
    mycursor.execute(line)
    results = mycursor.fetchall()
    return results