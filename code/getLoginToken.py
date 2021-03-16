import os
import yaml
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def loginToken():
    current_directory = os.path.dirname(os.path.realpath(__file__))

    with open(current_directory + '\\config.yaml', 'r') as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)

    tokenUrl = config['url'] + "/api/aaaLogin.json"
    tokenBody = json.dumps(
        {
            "aaaUser": {
                "attributes": {
                    "name": config['aaaUsername'],
                    "pwd": config['aaaPassword']
                }
            }
        }
    )
    tokenHeader = {'Content-Type': 'application/json'}
    r = requests.post(tokenUrl, data=tokenBody, headers=tokenHeader, verify=False)
    tokenJson = r.json()
    loginData = tokenJson['imdata']
    for loginInfo in loginData:
        loginToken = loginInfo['aaaLogin']['attributes']['token']
    return loginToken


if __name__ == '__main__':
    print(loginToken())
