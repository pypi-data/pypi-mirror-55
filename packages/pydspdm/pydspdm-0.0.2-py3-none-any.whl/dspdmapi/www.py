import requests
import json

def getWellData():
    url = "http://10.134.192.116:8081/dspdm/rest/common/WELL"
    response = requests.request("GET", url)
    python_obj = json.loads(response.text)
    data = python_obj["data"]
    well = data["WELL"]["list"]
    return well