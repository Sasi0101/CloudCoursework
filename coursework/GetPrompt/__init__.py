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
    container_prompt = database.get_container_client(CONTAINER_PROMPT)

    all_prompts = list(container_prompt.query_items(query = "SELECT * FROM c", enable_cross_partition_query= True))
    final_submit = []
    input = req.get_json()

    if("prompts" in input.keys()):
        number_of_prompts_needed = input["prompts"]

        #if n>prompts number return all
        if(len(all_prompts) <= number_of_prompts_needed):
            for i in range (len(all_prompts)):
                final_submit.append({"id": all_prompts[i]["id"], "text": all_prompts[i]["text"], "username": all_prompts[i]["username"]})
            return func.HttpResponse(json.dumps(final_submit))
        
        #if n < prompts
        random_numbers = random.sample(range(0, len(all_prompts)), number_of_prompts_needed)
        for i in range(number_of_prompts_needed):
            final_submit.append({"id": all_prompts[random_numbers[i]]["id"], "text": all_prompts[random_numbers[i]]["text"], "username": all_prompts[random_numbers[i]]["username"]})
        
    else:
        usernames = input["players"]
        #get all the stories that we need
        for i in range(len(usernames)):
            to_append = list(container_prompt.query_items(query = 
        "SELECT c.id, c.text, c.username FROM c WHERE c.username=\"" + usernames[i] + "\"", enable_cross_partition_query=True))


        if(len(to_append) != 0):
            for i in range(len(to_append)):
                final_submit.append(to_append[i])

    return func.HttpResponse(json.dumps(final_submit))