import requests
import json

url = "http://localhost:3000/login"
response = requests.post(url,params={"username":"旺旺","password":"喵喵"})