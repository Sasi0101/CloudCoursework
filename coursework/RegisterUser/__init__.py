import logging
import json
import azure.functions as func
from azure.cosmos import CosmosClient
DATABASE_NAME = "MainContainer"
CONTAINER_NAME = "RegisteredUsers"
URL = "https://coursework.documents.azure.com:443/"
KEY = "LLqDlNjStpwAFL07vYlVFw9gKpbv693bc0BJsQ8PjGiKyGLk0fmLFrRmx1tGUepptUcCONiXefTknJi193HtIQ=="



def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    player = req.get_json()
    username = player["username"]
    password = player["password"]


    if (len(username) > 16 or len(username) < 4):
        return func.HttpResponse(json.dumps({"result": False, "msg": "Username less than 4 characters or more than 16 characters" }))
    elif (len(password) > 24 or len(password) < 8):
        return func.HttpResponse(json.dumps({"result": False, "msg": "Password less than 8 characters or more than 24 characters" }))
    else:
        player_list = container.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  username + "\"", enable_cross_partition_query=True)
        if len(list(player_list)) == 0:
            container.create_item({"username" : username,
                "password" : password,
                "games_played" : 0,
                "total_score" : 0},
                enable_automatic_id_generation=True)
            return func.HttpResponse(json.dumps({"result": True, "msg": "OK" }))
        else:
            return func.HttpResponse(json.dumps({"result": False, "msg": "User already exists" }))