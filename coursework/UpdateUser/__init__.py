import logging
import json
import azure.functions as func
from azure.cosmos import CosmosClient
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
    addToGamesPlayed = 0
    addToScore = 0

    user = req.get_json()
    username = user["username"]
    password = user["password"]
    #find the user that needs to be updated
    user_list = list(container.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  username + "\"", enable_cross_partition_query=True))

    #check if the user exists
    if len(user_list) == 0:
        return func.HttpResponse(json.dumps({"result": False, "msg": "user does not exist" }))

    ourUser = user_list[0]

    #check if the password is correct
    if(password != ourUser["password"]):
        return func.HttpResponse(json.dumps({"result": False, "msg": "wrong password"}))

    
    #change the addToGamesPlayed if needed
    if("add_to_games_played" in user.keys()):
        if(user["add_to_games_played"] <=0 ):
            return func.HttpResponse(json.dumps({"result": False, "msg": "Value to add is <=0"}))
        else:
            addToGamesPlayed = user["add_to_games_played"]

    #change the addtoScore
    if("add_to_score" in user.keys()):
        if(user["add_to_score"] <=0 ):
            return func.HttpResponse(json.dumps({"result": False, "msg": "Value to add is <=0"}))
        else:
            addToScore = user["add_to_score"]
    
    newScore = ourUser["total_score"] + addToScore
    newGamesPlayed = ourUser["games_played"] + addToGamesPlayed
    container.replace_item(item = ourUser["id"], body = {"username": username, "password": password, "games_played": newGamesPlayed, "total_score": newScore, "id": ourUser["id"]})

    return func.HttpResponse(json.dumps({"result": True, "msg": "OK"}))
    

