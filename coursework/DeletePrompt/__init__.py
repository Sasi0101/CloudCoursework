import logging
from azure.cosmos import CosmosClient
import azure.functions as func
import json
import uuid
import config

DATABASE_NAME = config.settings["db_id"]
CONTAINER_USERS = config.settings["CONTAINER_USERS"]
CONTAINER_PROMPT = config.settings["CONTAINER_PROMPT"]
URL = config.settings["db_URI"]
KEY = config.settings["db_key"]


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container_users = database.get_container_client(CONTAINER_USERS)
    container_prompt = database.get_container_client(CONTAINER_PROMPT)

    input = req.get_json()
    id = str(input["id"])
    username = input ["username"]
    password = input["password"]

    user_list = list(container_users.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  username + "\" AND c.password=\"" + password + "\" ", enable_cross_partition_query=True))

    #check if username and password are correct
    if len(user_list) == 0:
        return func.HttpResponse(json.dumps({"result": False, "msg": "bad username or password"}))  

    #check if the id exists
    user_id = list(container_prompt.query_items(query = "SELECT c.username FROM c WHERE c.id=\"" +  id + "\"", enable_cross_partition_query= True))
    if(len(user_id) == 0):
        return func.HttpResponse(json.dumps({"result": False, "msg": "prompt id does not exist"}))
    
    #check if the user has access
    if(user_id[0]["username"] != username):
        return func.HttpResponse(json.dumps({"result": False, "msg": "access denied"}))

    #if no error so far we delete it
    container_prompt.delete_item(item = id, partition_key=id)


    return func.HttpResponse(json.dumps({"result": True, "msg":"OK"}))


