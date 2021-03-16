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

### Create Filter ###
tenant = "common"
filterName = "Russel-Filter-common-03"
filterEntryName = "Russel-Filter-Entry-common-03"
sourcePort = "22"
destinationPort = "22"
ethernetType = "ip"
protocol = "6"

url = config['url'] + "/api/node/mo/uni/tn-" + tenant + "/flt-" + filterName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
	"vzFilter": {
		"attributes": {
			"name": filterName,
			"status": "created"
		},
		"children": [
			{
				"vzEntry": {
					"attributes": {
						"dFromPort": sourcePort,
						"dToPort": destinationPort,
						"etherT": ethernetType,
						"name": filterEntryName,
						"prot": protocol,
						"status": "created"
					},
					"children": []
				}
			}
		]
	}
}

# print(payload)

r = requests.post(url, headers=headers, json=payload, verify=False)
rjson = r.json()

print(rjson)