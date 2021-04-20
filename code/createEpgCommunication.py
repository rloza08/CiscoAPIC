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

# Variables
tenant = "az-acitest-nonprod-02"
appProfileProviderName = "Russel-Provider-AppProfile-318-01"
appProfileConsumerName = "Russel-Consumer-AppProfile-318-01"
cloudEpgProviderName = "Russel-EPG-Provider-318-01"
cloudEpgConsumerName = "Russel-EPG-Consumer-318-01"
contractName = "Russel-Contract-318-01"
serviceGraphName = "Russel-ServiceGraph-318-01"
cloudListenerName = "Russel-listener-22"
cloudListenerPort = "22"
cloudListenerProtocol = "tcp"

# Create EPG Communication
url = config['url'] + "/api/node/mo/uni/tn-" + tenant + ".json"
headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Cookie': 'APIC-cookie=' + loginToken}
payload = {
    "fvTenant": {
        "attributes": {
            "name": tenant
        },
        "children": [
            {
                "cloudApp": {
                    "attributes": {
                        "name": appProfileProviderName
                    },
                    "children": [
                        {
                            "cloudEPg": {
                                "attributes": {
                                    "name": cloudEpgProviderName
                                },
                                "children": [
                                    {
                                        "fvRsProv": {
                                            "attributes": {
                                                "tnVzBrCPName": contractName
                                            },
                                            "children": []
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "cloudApp": {
                    "attributes": {
                        "name": appProfileConsumerName
                    },
                    "children": [
                        {
                            "cloudEPg": {
                                "attributes": {
                                    "name": cloudEpgConsumerName
                                },
                                "children": [
                                    {
                                        "fvRsCons": {
                                            "attributes": {
                                                "tnVzBrCPName": contractName
                                            },
                                            "children": []
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            {
                "vnsAbsGraph": {
                    "attributes": {
                        "name": serviceGraphName
                    },
                    "children": [
                        {
                            "vnsAbsNode": {
                                "attributes": {
                                    "name": "N0"
                                },
                                "children": [
                                    {
                                        "cloudSvcPolicy": {
                                            "attributes": {
                                                "contractName": contractName,
                                                "subjectName": "default",
                                                "tenantName": tenant
                                            },
                                            "children": [
                                                {
                                                    "cloudListener": {
                                                        "attributes": {
                                                            "name": cloudListenerName,
                                                            "port": cloudListenerPort,
                                                            "protocol": cloudListenerProtocol,
                                                            "status": "created"
                                                        },
                                                        "children": [
                                                            {
                                                                "cloudListenerRule": {
                                                                    "attributes": {
                                                                        "default": "true",
                                                                        "name": "default"
                                                                    },
                                                                    "children": [
                                                                        {
                                                                            "cloudRuleAction": {
                                                                                "attributes": {
                                                                                    "epgdn": "uni/tn-" + tenant + "/cloudapp-" + appProfileProviderName + "/cloudepg-" + cloudEpgProviderName,
                                                                                    "healthProbe": "default_" + cloudListenerName,
                                                                                    "port": cloudListenerPort,
                                                                                    "protocol": cloudListenerProtocol,
                                                                                    "type": "forward"
                                                                                },
                                                                                "children": []
                                                                            }
                                                                        }
                                                                    ]
                                                                }
                                                            }
                                                        ]
                                                    }
                                                },
                                                {
                                                    "cloudHealthProbe": {
                                                        "attributes": {
                                                            "interval": "5",
                                                            "name": "default_" + cloudListenerName,
                                                            "port": cloudListenerPort,
                                                            "protocol": cloudListenerProtocol,
                                                            "status": "created",
                                                            "unhealthyThreshold": "2"
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
                    ]
                }
            },
            {
                "vzBrCP": {
                    "attributes": {
                        "name": contractName
                    },
                    "children": [
                        {
                            "vzSubj": {
                                "attributes": {
                                    "name": "default"
                                },
                                "children": [
                                    {
                                        "vzRsSubjGraphAtt": {
                                            "attributes": {
                                                "tnVnsAbsGraphName": serviceGraphName
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
        ]
    }
}

# print(payload)

r = requests.post(url, headers=headers, json=payload, verify=False)
rjson = r.json()

print(rjson)
