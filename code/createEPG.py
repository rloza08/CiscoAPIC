import os
import yaml
import json
import requests
import time
from getLoginToken import loginToken
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
current_directory = os.path.dirname(os.path.realpath(__file__))

with open(current_directory + "\\config.yaml", "r") as yamlfile:
	config = yaml.load(yamlfile, Loader=yaml.FullLoader)

loginToken = loginToken()
time.sleep(1)

### Post EPG ###
tenant = "az-acitest-npr-02"
appProfileName = "Russel-AppProfile-20"
cloudEpgName = "Russel-Test-EPG-22"
vrf = "nonprod"

print(loginToken)

# add script that creates app profile
# add EPG selector

url = config['url'] + "/api/node/mo/uni/tn-" + tenant + "/cloudapp-" + appProfileName + "/cloudepg-" + cloudEpgName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
	"cloudEPg": {
		"attributes": {
			"name": cloudEpgName,
			"status": "created"
		},
		"children": [
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