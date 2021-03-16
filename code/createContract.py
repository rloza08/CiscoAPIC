import os
import yaml
import json
import requests
from getLoginToken import loginToken
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
current_directory = os.path.dirname(os.path.realpath(__file__))
with open(current_directory + "\\config.yaml", "r") as yamlfile:
	config = yaml.load(yamlfile, Loader=yaml.FullLoader)

loginToken = loginToken()
# print(loginToken)

### Create Contract ###
tenant = "az-acitest-nonprod-02"
contractName = "Russel-Contract-39-01"
scope = "tenant"
filterName = "Russel-Filter-common-03"

url = config['url'] + "/api/node/mo/uni/tn-" + tenant + "/brc-" + contractName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
	"vzBrCP": {
		"attributes": {
			"name": contractName,
			"scope": scope,
			"status": "created"
		},
		"children": [
			{
				"vzSubj": {
					"attributes": {
						"name": "default"
					},
					"children": [
						{
							"vzRsSubjFiltAtt": {
								"attributes": {
									"action": "permit",
									"status": "created",
									"tnVzFilterName": filterName
								},
								"children": []
							}
						}
					]
				}
			}
		]
	}
}

# print(payload)

r = requests.post(url, headers=headers, json=payload, verify=False)
rjson = r.json()

print(rjson)