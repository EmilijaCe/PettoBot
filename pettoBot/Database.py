
'''
import mysql.connector
#con = mysql.connector.connect(host = 'localhost', user = 'root', password = main.DBpassword, database = 'bots')
#con = mysql.connector.connect(host = 'pettobot-server.mysql.database.azure.com', user = 'efkabvewnb', password = password, database = 'pettobot-database')
#con = mysql.connector.connect(user="efkabvewnb", password=main.DBpassword, host="pettobot-server.mysql.database.azure.com", port=3306, database="pettobot-database", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)
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
    return results'''


import azure.cosmos.cosmos_client as cosmos_client
import configs

HOST = configs.settings['host']
MASTER_KEY = configs.settings['master_key']
DATABASE_ID = configs.settings['database_id']
CONTAINER_ID = configs.settings['container_id']

client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
db = client.get_database_client(DATABASE_ID)
container = db.get_container_client(CONTAINER_ID)

def insert(items, values):
    line = {}
    for i in range(len(items)):
        line[items[i]] = str(values[i])
    
    container.create_item(body=line)


def select(items, whereitem = None, wherevalue = None):
    line = "SELECT * FROM c"
    if whereitem != None:
        line += " WHERE c." + str(whereitem) + " = \"" + str(wherevalue) + "\""
    
    results = []
    
    for found in container.query_items(query = line, enable_cross_partition_query=True):
        itemlist = []
        for item in items:
            itemlist.append(found[item])
        results.append(itemlist)
    
    return results

def update(items, values, whereitem, wherevalue):
    line = f"SELECT * FROM c WHERE c.{whereitem} = \"{wherevalue}\""
    for found in container.query_items(query = line, enable_cross_partition_query=True):
        for i in range(len(items)):
            found[items[i]] = str(values[i])
        container.replace_item(item=found, body=found)