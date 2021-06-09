from base64 import b64encode
import requests
import json
import os
from dotenv import load_dotenv

# load all environment variables
load_dotenv()

#Build the Headers for the API Calls to ISE
def build_headers():
    authencode = os.environ['API_USER']+":"+os.environ['API_PASS']
    authencode = authencode.encode("ascii")
    userAndPass = b64encode(authencode).decode("ascii")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic %s" % userAndPass
        }
    return headers

#Build the JSON Payload with the AWS System Info Mapped to ISE Custom Attributes
def build_payload_aws(vcInfo, mac):
    payload = {
        "ERSEndPoint": {
            "mac": mac,
            "customAttributes": {
                "customAttributes": {
                    "PrivateIpAddress": vcInfo["PrivateIpAddress"],
                    "PrivateDnsName": vcInfo["PrivateDnsName"],
                    "ImageId": vcInfo["ImageId"],
                    "SecurityGroup": vcInfo["SecurityGroup"],
                    "state": vcInfo["state"],
                    "fisma_tag" : "tag_placeholder"
                    }
                }
            }
        }
    return payload

#Build the JSON Payload with the Azure System Info Mapped to ISE Custom Attributes
def build_payload_azure(vcInfo, mac):
    payload = {
        "ERSEndPoint": {
            "mac": mac,
            "customAttributes": {
                "customAttributes": {
                    "VMID": vcInfo["uuid"],
                    "OS": vcInfo["osName"],
                    "private_ip" : vcInfo["private_ip"],
                    "fisma_tag" : "tag_placeholder"
                    }
                }
            }
        }
    return payload

#Get the Endpoint ID from ISE by Searching on MAC Address
def get_endpoint_id_by_mac(mac):
    headers = build_headers()
    url = "https://"+os.environ['API_HOST']+":9060/ers/config/endpoint/name/"+mac
    try:
        response = requests.request("GET", url, data="{}", headers=headers, verify=False)
        endpointData = json.loads(response.text.encode("utf8"))
        endpointId = endpointData["ERSEndPoint"]["id"]
    except:
        endpointId = None
    return endpointId

#Push the Custom Attributes to ISE   
def update_endpoint(endpointId, payload):
    headers = build_headers()
    if endpointId != None:
        url = "https://"+os.environ['API_HOST']+":9060/ers/config/endpoint/"+endpointId
        response = requests.request("PUT", url, data=json.dumps(payload), headers=headers, verify=False)
    else:
        url = "https://"+os.environ['API_HOST']+":9060/ers/config/endpoint/"
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)
    return response

#Main Module Logic and Logging
def endpoint(vcInfo, mac,type):
    endpointId = get_endpoint_id_by_mac(mac)
    if type == "aws":
        payload = build_payload_aws(vcInfo, mac)
    if type == "azure":
        payload = build_payload_azure(vcInfo, mac)
    response = update_endpoint(endpointId, payload)