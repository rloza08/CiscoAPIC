import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

tokenUrl = "https://168.61.65.109/api/aaaLogin.json"
tokenBody = """{ 
        "aaaUser": { 
            "attributes": { 
                "name": "ScriptUser", 
                "pwd": "Scr1ptUs3r37*~" 
            } 
        } 
    }"""
tokenHeader = {'Content-Type': 'application/json'}
r = requests.post(tokenUrl, data=tokenBody, headers=tokenHeader, verify=False)
tokenJson = r.json()
loginData = tokenJson['imdata']
for loginInfo in loginData:
    loginToken = loginInfo['aaaLogin']['attributes']['token']

print(loginToken)
