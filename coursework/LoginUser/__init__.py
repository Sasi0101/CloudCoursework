import json
import azure.functions as func
from azure.cosmos import CosmosClient
import logging

DATABASE_NAME = "MainContainer"
CONTAINER_NAME = "RegisteredUsers"
URL = "https://coursework.documents.azure.com:443/"
KEY = "LLqDlNjStpwAFL07vYlVFw9gKpbv693bc0BJsQ8PjGiKyGLk0fmLFrRmx1tGUepptUcCONiXefTknJi193HtIQ=="


def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    
    user = req.get_json()
    username = user["username"]
    password = user["password"]

    user_list = container.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  username + "\" AND c.password=\"" + password + "\" ", enable_cross_partition_query=True)
    if len(list(user_list)) > 0:
        return func.HttpResponse(json.dumps({"result": True, "msg": "OK" }))
    else:
        return func.HttpResponse(json.dumps({"result": False, "msg": "Username or password incorrect" }))

    
