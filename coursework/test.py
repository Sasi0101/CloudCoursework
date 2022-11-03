import logging
import uuid
import azure.functions as func
from azure.cosmos import CosmosClient

DATABASE_NAME = "MainContainer"
CONTAINER_NAME = "RegisteredUsers"
URL = "https://coursework.documents.azure.com:443/"
KEY = "LLqDlNjStpwAFL07vYlVFw9gKpbv693bc0BJsQ8PjGiKyGLk0fmLFrRmx1tGUepptUcCONiXefTknJi193HtIQ=="



class main():

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    
    payload = {"username": "most", "password": "csakmost"}
    query_result = container.query_items(query = """SELECT * FROM c""", enable_cross_partition_query=True)

    container.create_item({"username" : payload["username"],
                        "password" : payload["password"],
                        "games_played" : 0,
                        "total_score" : 0,
                        "id": str(uuid.uuid1())})
    print(list(query_result))

   
