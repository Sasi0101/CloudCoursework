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

    howMany = req.get_json()["top"]

    #get the list of all the users with the highest values
    user_list = list(container.query_items(query = "SELECT * FROM c", enable_cross_partition_query=True))
    
    new_user_list = []
    for users in user_list:
        new_user_list.append({"username": users["username"], "score": users["total_score"], "games_played": users["games_played"]})
    
    #list sorted by score
    sorted_list_by_score = sorted(new_user_list, key = lambda x: (x["score"]), reverse = True)

    sort_username_list = []
    final_sorted_list = []
    for i in range(len(sorted_list_by_score)):

        #check if i is the last one
        if(i == len(sorted_list_by_score)-1):
            if(sorted_list_by_score[i]["score"] == sorted_list_by_score[i-1]["score"]):
                sort_username_list.append(sorted_list_by_score[i])
                temp = sorted(sort_username_list, key = lambda x: (x["username"]))
                for t in temp:
                    final_sorted_list.append(t)
                sort_username_list.clear()
                temp.clear()
            else: 
                final_sorted_list.append(sorted_list_by_score[i])
        else:
            if(sorted_list_by_score[i]["score"] == sorted_list_by_score[i+1]["score"]):
                sort_username_list.append(sorted_list_by_score[i])
            else:
                if(len(sort_username_list) == 0):
                    final_sorted_list.append(sorted_list_by_score[i])
                else:
                    temp = sorted(sort_username_list, key = lambda x: (x["username"]))
                    for t in temp:
                        final_sorted_list.append(t)
                    sort_username_list.clear()
                    temp.clear()

    if(howMany >= len(final_sorted_list)):
        final_one = final_sorted_list
    else:
        final_one = final_sorted_list[0:howMany]

    #for users in sorted_list_by_score:
        

        
    return func.HttpResponse(json.dumps(final_one))
    

