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
print(loginToken)

### Post NLB Service ###
tenant = "az-acitest-nonprod-02"
serviceName = "Russel-LB-38-02"
customRG = "az-acitest-nonprod-02-network-sb-westus-rg-01"
serviceType = "network"
scheme = "internal"
cloudContextProfile = "az-acitest-nonprod-02"
subnet = "10.1.0.0/28"
cidr = "10.1.0.0/22"

url = config['url'] + "/api/node/mo/uni/tn-" + tenant + "/clb-" + serviceName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
    "cloudLB": {
        "attributes": {
            "customRG": customRG,
            "name": serviceName,
            "scheme": scheme,
            "status": "",
            "type": serviceType
        },
        "children": [
            {
                "cloudRsLDevToCloudSubnet": {
                    "attributes": {
                        "tDn": "uni/tn-" + tenant + "/ctxprofile-" + cloudContextProfile + "/cidr-[" + cidr + "]/subnet-[" + subnet + "]"
                    },
                    "children": []
                }
            }
        ]
    }
}

print(payload)

r = requests.post(url, headers=headers, json=payload, verify=False)
rjson = r.json()

print(rjson)
