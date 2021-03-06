import os
import yaml
import requests
from getLoginToken import loginToken
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
current_directory = os.path.dirname(os.path.realpath(__file__))
with open(current_directory + "\\config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

loginToken = loginToken()

# Variables
# 	Application Profile
tenant = "az-acitest-nonprod-02"
appProfileName = "Russel-Provider-AppProfile-318-01"
# 	EPG
cloudEpgName = "Russel-EPG-Consumer-318-01"
matchExpression = "custom:role=='web',custom:snet=='ngcp-qa-snet',custom:environment=='qa2',custom:appcode=='ngcp'"
cloudEPSelectorName = "Russel-EndpointSelector-318-01"
vrf = "nonprod"

# Create Application Profile
url = config['url'] + "/api/node/mo/uni/tn-" + tenant + "/cloudapp-" + appProfileName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
    "cloudApp": {
        "attributes": {
            "descr": appProfileName,
            "name": appProfileName,
            "status": "created"
        },
        "children": []
    }
}

r = requests.post(url, headers=headers, json=payload, verify=False)
rjson = r.json()

print(rjson)

# Create EPG
url = config[
          'url'] + "/api/node/mo/uni/tn-" + tenant + "/cloudapp-" + appProfileName + "/cloudepg-" + cloudEpgName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
    "cloudEPg": {
        "attributes": {
            "name": cloudEpgName,
            "status": "created"
        },
        "children": [
            {
                "cloudEPSelector": {
                    "attributes": {
                        "matchExpression": matchExpression,
                        "name": cloudEPSelectorName,
                        "status": "created"
                    },
                    "children": []
                }
            },
            {
                "cloudRsCloudEPgCtx": {
                    "attributes": {
                        "status": "",
                        "tnFvCtxName": vrf
                    },
                    "children": []
                }
            }
        ]
    }
}

r = requests.post(url, headers=headers, json=payload, verify=False)
rjson = r.json()

print(rjson)
