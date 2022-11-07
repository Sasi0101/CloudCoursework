import json
import azure.functions as func
from azure.cosmos import CosmosClient
import logging
import config

DATABASE_NAME = config.settings["db_id"]
CONTAINER_USERS = config.settings["CONTAINER_USERS"]
CONTAINER_PROMPT = config.settings["CONTAINER_PROMPT"]
URL = config.settings["db_URI"]
KEY = config.settings["db_key"]



def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_USERS)
    
    user = req.get_json()
    username = user["username"]
    password = user["password"]

    user_list = container.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  username + "\" AND c.password=\"" + password + "\" ", enable_cross_partition_query=True)
    if len(list(user_list)) > 0:
        return func.HttpResponse(json.dumps({"result": True, "msg": "OK" }))
    else:
        return func.HttpResponse(json.dumps({"result": False, "msg": "Username or password incorrect" }))

    
