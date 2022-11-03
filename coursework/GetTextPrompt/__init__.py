from azure.cosmos import CosmosClient
import azure.functions as func
import json
import random

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
    word = input["word"]
    exact = input["exact"]

    all_prompts = list(container_prompt.query_items(query="SELECT * FROM c", enable_cross_partition_query= True))

    final_submit = []

    if not exact:
        for i in range(len(all_prompts)):
            if (word in all_prompts[i]["text"]):
                final_submit.append({"id":all_prompts[i]["id"], "text": all_prompts[i]["text"], "username": all_prompts[i]["username"]})
    else:
        for i in range(len(all_prompts)):
            words_of_text = all_prompts[i]["text"].split()
            for k in range(len(words_of_text)):
                if(word == words_of_text[k]):
                    final_submit.append({"id":all_prompts[i]["id"], "text": all_prompts[i]["text"], "username": all_prompts[i]["username"]})




    return func.HttpResponse(json.dumps(final_submit))
    