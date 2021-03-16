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

# Variables
	# Network Load Balancer Service
tenant = "az-acitest-nonprod-02"
networkLoadBalancerName = "Russel-LB-39-01"
customRG = "az-acitest-nonprod-02-network-sb-westus-rg-01"
serviceType = "network"
scheme = "internal"
cloudContextProfile = "az-acitest-nonprod-02"
subnet = "10.1.0.0/28"
cidr = "10.1.0.0/22"
	# Service Graph
serviceGraphName = "Russel-ServiceGraph-39-01"

	# Create Network Load Balancer Service
url = config['url'] + "/api/node/mo/uni/tn-" + tenant + "/clb-" + networkLoadBalancerName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
	"cloudLB": {
		"attributes": {
			"customRG": customRG,
			"name": networkLoadBalancerName,
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

# print(payload)
r = requests.post(url, headers=headers, json=payload, verify=False)
rjson = r.json()
print(rjson)

### Post Service Graph ###
url = config['url'] + "/api/node/mo/uni/tn-" + tenant + "/AbsGraph-" + serviceGraphName + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
	"vnsAbsGraph": {
		"attributes": {
			"name": serviceGraphName,
			"status": "created",
			"type": "cloud"
		},
		"children": [
			{
				"vnsAbsTermNodeCon": {
					"attributes": {
						"name": "T1"
					},
					"children": [
						{
							"vnsAbsTermConn": {
								"attributes": {
									"name": "ConsTermConn"
								},
								"children": []
							}
						}
					]
				}
			},
			{
				"vnsAbsNode": {
					"attributes": {
						"funcTemplateType": "ADC_ONE_ARM",
						"funcType": "GoTo",
						"managed": "yes",
						"name": "N0"
					},
					"children": [
						{
							"vnsRsNodeToCloudLDev": {
								"attributes": {
									"tDn": "uni/tn-" + tenant + "/clb-" + networkLoadBalancerName
								},
								"children": []
							}
						},
						{
							"vnsAbsFuncConn": {
								"attributes": {
									"attNotify": "no",
									"connType": "none",
									"name": "provider"
								},
								"children": []
							}
						},
						{
							"vnsAbsFuncConn": {
								"attributes": {
									"attNotify": "no",
									"connType": "none",
									"name": "consumer"
								},
								"children": []
							}
						}
					]
				}
			},
			{
				"vnsAbsConnection": {
					"attributes": {
						"adjType": "L3",
						"connDir": "provider",
						"connType": "external",
						"name": "CON0"
					},
					"children": [
						{
							"vnsRsAbsConnectionConns": {
								"attributes": {
									"tDn": "uni/tn-" + tenant + "/AbsGraph-" + serviceGraphName + "/AbsTermNodeCon-T1/AbsTConn"
								},
								"children": []
							}
						},
						{
							"vnsRsAbsConnectionConns": {
								"attributes": {
									"tDn": "uni/tn-" + tenant + "/AbsGraph-" + serviceGraphName + "/AbsNode-N0/AbsFConn-consumer"
								},
								"children": []
							}
						}
					]
				}
			},
			{
				"vnsAbsConnection": {
					"attributes": {
						"adjType": "L3",
						"connDir": "provider",
						"connType": "external",
						"name": "CON1"
					},
					"children": [
						{
							"vnsRsAbsConnectionConns": {
								"attributes": {
									"tDn": "uni/tn-" + tenant + "/AbsGraph-" + serviceGraphName + "/AbsTermNodeProv-T2/AbsTConn"
								},
								"children": []
							}
						},
						{
							"vnsRsAbsConnectionConns": {
								"attributes": {
									"tDn": "uni/tn-" + tenant + "/AbsGraph-" + serviceGraphName + "/AbsNode-N0/AbsFConn-provider"
								},
								"children": []
							}
						}
					]
				}
			},
			{
				"vnsAbsTermNodeProv": {
					"attributes": {
						"name": "T2"
					},
					"children": [
						{
							"vnsAbsTermConn": {
								"attributes": {
									"name": "ProvTermConn"
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