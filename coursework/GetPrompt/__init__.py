from azure.cosmos import CosmosClient
import azure.functions as func
import json
import random
import config

DATABASE_NAME = config.settings["db_id"]
CONTAINER_USERS = config.settings["CONTAINER_USERS"]
CONTAINER_PROMPT = config.settings["CONTAINER_PROMPT"]
URL = config.settings["db_URI"]
KEY = config.settings["db_key"]

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
                for k in range(len(to_append)):
                    final_submit.append(to_append[k])
                to_append.clear()


    return func.HttpResponse(json.dumps(final_submit))