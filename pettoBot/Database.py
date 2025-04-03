import azure.cosmos.cosmos_client as cosmos_client


class Database:
    
    def __init__(self, HOST, MASTER_KEY, DATABASE_ID, CONTAINER_ID):
        self.client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        self.db = self.client.get_database_client(DATABASE_ID)
        self.container = self.db.get_container_client(CONTAINER_ID)
        

    def insert(self, items, values):
        line = {}
        for i in range(len(items)):
            line[items[i]] = str(values[i])
        
        self.container.create_item(body=line)


    def select(self, items, whereitem = None, wherevalue = None):
        line = "SELECT * FROM c"
        if whereitem != None:
            line += " WHERE c." + str(whereitem) + " = \"" + str(wherevalue) + "\""
        
        results = []
        
        for found in self.container.query_items(query = line, enable_cross_partition_query=True):
            itemlist = []
            for item in items:
                itemlist.append(found[item])
            results.append(itemlist)
        
        return results

    def update(self, items, values, whereitem, wherevalue):
        line = f"SELECT * FROM c WHERE c.{whereitem} = \"{wherevalue}\""
        for found in self.container.query_items(query = line, enable_cross_partition_query=True):
            for i in range(len(items)):
                found[items[i]] = str(values[i])
            self.container.replace_item(item=found, body=found)