from azure.cosmos import CosmosClient
import azure.functions as func
import json

DATABASE_NAME = "MainContainer"
CONTAINER_USERS = "RegisteredUsers"
CONTAINER_PROMPT = "Prompt"
URL = "https://coursework.documents.azure.com:443/"
KEY = "LLqDlNjStpwAFL07vYlVFw9gKpbv693bc0BJsQ8PjGiKyGLk0fmLFrRmx1tGUepptUcCONiXefTknJi193HtIQ=="

def main(req: func.HttpRequest) -> func.HttpResponse:

    client = CosmosClient(URL, credential=KEY)
    database = client.get_database_client(DATABASE_NAME)
    container_users = database.get_container_client(CONTAINER_USERS)
    container_prompt = database.get_container_client(CONTAINER_PROMPT)

    input = req.get_json()
    id = str(input["id"])
    text = input["text"]
    username = input ["username"]
    password = input["password"]

    user_list = list(container_users.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  username + "\" AND c.password=\"" + password + "\" ", enable_cross_partition_query=True))
    
    #check if username or password is correct
    if len(user_list) == 0:
        return func.HttpResponse(json.dumps({"result": False, "msg": "bad username or password"}))
    
    #check if the text is between 20-100 characters
    if (len(text) < 20 or len(text) > 100):
        return func.HttpResponse(json.dumps({"result": False, "msg": "prompt length is <20 or > 100 characters"}))
    
    #check if the user does not have this prompt already
    user_prompts = list(container_prompt.query_items(query = "SELECT * FROM c WHERE c.username=\"" +  username + "\"", enable_cross_partition_query=True))

    doesTHisPromptExist = False
    for prompts in user_prompts:
        if (prompts["text"] == text):
            doesTHisPromptExist = True

    if (doesTHisPromptExist):
        return func.HttpResponse(json.dumps({"result": False, "msg": "This user already has a prompt with the same text"}))

    #check if the id exists
    user_id = list(container_prompt.query_items(query = "SELECT * FROM c WHERE c.id=\"" +  id + "\"", enable_cross_partition_query= True))
    if(len(user_id) == 0):
        return func.HttpResponse(json.dumps({"result": False, "msg": "prompt id does not exist"}))

    #if we have no problem update the text
    container_prompt.replace_item(item = id, body = {"text": text, "username": username, "id": id})

    return func.HttpResponse(json.dumps({"result": True, "msg": "OK"}))



