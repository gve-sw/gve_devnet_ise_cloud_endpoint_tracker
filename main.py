# sdk packaged for Azure
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.identity import ClientSecretCredential
# sdk package for AWS
import boto3
# helper functions for ise api calls
import ise
import pprint
from base64 import b64encode
import base64
import requests
import json
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
import os
from datetime import datetime

# load all environment variables
load_dotenv()

def get_private(compute_client, network_client):
    for vm in compute_client.virtual_machines.list_all():
        for interface in vm.network_profile.network_interfaces:
            name=" ".join(interface.id.split('/')[-1:])
            sub="".join(interface.id.split('/')[4])

            try:
                thing=network_client.network_interfaces.get(sub, name).ip_configurations

                for x in thing:
                    return(x.private_ip_address)

            except Exception as e: print(e)

def get_mac(compute_client, network_client):
    for vm in compute_client.virtual_machines.list_all():
        for interface in vm.network_profile.network_interfaces:
            name=" ".join(interface.id.split('/')[-1:])
            sub="".join(interface.id.split('/')[4])

            try:
                thing=network_client.network_interfaces.get(sub, name).mac_address
                thing = thing.replace("-", ":")
                return thing

            except Exception as e: print(e)

def aws():

    print("Starting AWS process")
    print("----------------------------------------------")
    print("----------------------------------------------")

    # initializing aws client
    ec2 = boto3.client('ec2',region_name='us-east-1',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    # Retrieves all regions/endpoints that work with EC2
    response = ec2.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation["Instances"]:
            vmInfo = {}
            vmInfo["PrivateIpAddress"] = instance["PrivateIpAddress"]
            vmInfo["PrivateDnsName"] = instance["PrivateDnsName"]
            vmInfo["ImageId"] = instance["ImageId"]

            vmInfo["mac"] = instance["NetworkInterfaces"][0]["MacAddress"]
            vmInfo["SecurityGroup"] = instance["SecurityGroups"][0]["GroupName"]
            vmInfo["state"] = instance["State"]["Name"]

            pprint.pprint(instance)
            ise.endpoint(vmInfo, vmInfo["mac"],type="aws")
            # datetime object containing current date and time
            now = datetime.now()
            file_obj = open("log.txt","a")
            file_obj.write("VM " + vmInfo["PrivateDnsName"] + " from AWS pushed to ISE " + str(now) + "\n")
            file_obj.close()


def azure():

    print("starting azure process")
    print("----------------------------------------------")
    print("----------------------------------------------")
    credential = ClientSecretCredential(
        tenant_id=os.environ['AZURE_TENANT_ID'],
        client_id=os.environ['AZURE_CLIENT_ID'],
        client_secret=os.environ['AZURE_CLIENT_SECRET'])

    compute_client = ComputeManagementClient(
        credential=credential,
        subscription_id=os.environ['AZURE_SUBSCRIPTION_ID'],
        api_version='2020-12-01')

    network_client = NetworkManagementClient(credential,os.environ['AZURE_SUBSCRIPTION_ID'])

    vm_list = compute_client.virtual_machines.list_all()

    for vm in vm_list:
        array = vm.id.split("/")
        resource_group = array[4]
        vm_name = array[-1]
        statuses = compute_client.virtual_machines.instance_view(resource_group, vm_name)
        vm = compute_client.virtual_machines.get(resource_group, vm_name)
        nic_name = vm.network_profile.network_interfaces[0].id.split('/')[-1]
        nic_group = vm.network_profile.network_interfaces[0].id.split('/')[-5]

        vmInfo = {}
        vmInfo["osName"] = str(vm.instance_view.os_name) + " " + str(vm.instance_view.os_version)
        vmInfo["uuid"] = vm.vm_id
        vmInfo["mac"] = get_mac(compute_client, network_client)

        vmInfo["private_ip"] = get_private(compute_client, network_client)
        ise.endpoint(vmInfo, vmInfo["mac"],type="azure")
        # datetime object containing current date and time
        now = datetime.now()
        file_obj = open("log.txt","a")
        file_obj.write("VM " + vmInfo["uuid"] + " from AZURE pushed to ISE " + str(now) + "\n")
        file_obj.close()


scheduler = BlockingScheduler()
scheduler.add_job(aws, 'interval', minutes=1)
scheduler.add_job(azure, 'interval', minutes=1)
scheduler.start()