import requests 
import unittest
import azure.functions as func
from azure.cosmos import CosmosClient
from RegisterUser import main
import RegisterUser

DATABASE_NAME = 'MainContainer'
CONTAINER_NAME = 'RegisteredUsers'
URL = "https://coursework.documents.azure.com:443/"
KEY = "LLqDlNjStpwAFL07vYlVFw9gKpbv693bc0BJsQ8PjGiKyGLk0fmLFrRmx1tGUepptUcCONiXefTknJi193HtIQ=="


class TestFunction(unittest.TestCase):
    def test_loginPlayer(self):
        # Instead of a mock HTTP request.
        # We make a real HTTP request, passing our mock stories as parameters
        payload = {"username": "test333", "password": "nowaydude"}

        resp = requests.get(
                "https://coursework-sk10g20.azurewebsites.net/api/player/register", 
                json = payload)
        
        #self.assertEqual(resp['msg'],'OK')
        #output = resp.json()
        #print(output)
        #self.assertEqual(len(listOfContainer), 9)
        
        