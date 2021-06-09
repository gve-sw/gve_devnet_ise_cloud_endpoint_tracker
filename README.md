# GVE_DevNet_ISE_Cloud_Endpoint_Tracker
prototype script that collects information from AWS and Azure virtual machines and creates an endpoint profile into ISE instance


## Contacts
* Jorge Banegas

## Solution Components
* AWS
* AZURE
* ISE
* PYTHON

## Installation/Configuration

Make sure you are on the root of the project folder. 

1. First step will be to include the credentials of your ISE/AWS/AZURE instances into the .env file

```python
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AZURE_SUBSCRIPTION_ID=
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
API_HOST=
API_USER=
API_PASS=
```

2. To find your AWS AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, log into your AWS portal and click on your username, then on my Security Credetials. Scroll down and click on create access key. Copy both and enter it in the .env file.

![/IMAGES/aws_step1.png](/IMAGES/aws_step1.png)

3. To find your AZURE_TENANT_ID and AZURE_CLIENT_ID, log into your Azure portal and select the Azure Active Directory service and on the left panel, click on App  registrations then New registration. Once you create the app registration, copy the  AZURE_TENANT_ID and AZURE_CLIENT_ID.

![/IMAGES/azure_step1.png](/IMAGES/azure_step1.png)

4. To find your AZURE_CLIENT_SECRET, click on the App Registration you just created and on the left panel, click on Certificates and secrets. Generate your Client Secret and copy that. 

![/IMAGES/azure_step1.png](/IMAGES/azure_step2.png)

5. To find your AZURE_SUBSCRIPTION_ID log into your Azure portal and select the subscription service and copy the subscription ID.

![/IMAGES/azure_step3.png](/IMAGES/azure_step3.png)

6. Enter the IP address and credentials for your ISE environment. Now you have all the required fields for this script.

7. Log into your ISE instance and create the custom attributes. 

![/IMAGES/ise_attributes.png](/IMAGES/ise_attributes.png)

It is important to use the same case senstivity. The attribute names have to mirror what is on the python script. You can refer to this image 

![/IMAGES/script_attributes.png](/IMAGES/script_attributes.png)

7. Create virtual environment and name it env, then activate it

```console
foo@bar:~$ virtualenv env
foo@bar:~$ source env/bin/activate
```

8. Install the dependencies required for the python script
```console
foo@bar(env):~$ pip install -r requirements.txt
```

You can change the time frequency of the queries by minutes in line 125 and 126

```console
scheduler.add_job(aws, 'interval', minutes=1)
scheduler.add_job(azure, 'interval', minutes=1)
```

## Usage

To launch script:


    ```console
    foo@bar(env):~$ python main.py
    ```
Or you may use the Dockerfile to run it as well 
   ```console
    foo@bar(env):~$ docker build -t iseimage:1.0 .
    foo@bar(env):~$ docker container run --name iseimage
   ```

# Screenshots

Snapshot of my AWS and Azure environment

![/IMAGES/aws_ec2.png](/IMAGES/aws_ec2.png)

![/IMAGES/azure_vms.png](/IMAGES/azure_vms.png)

ISE before launching script

![/IMAGES/before_script.png](/IMAGES/before_script.png)

ISE after launching script

![/IMAGES/after_script.png](/IMAGES/after_script.png)

Snapshot of an AWS endpoint on ISE

![/IMAGES/aws_endpoint.png](/IMAGES/aws_endpoint.png)

Snapshot of an AZURE endpoint on ISE

![/IMAGES/azure_endpoint.png](/IMAGES/azure_endpoint.png)

# Additional Resources

* Check out the AWS python SDK link if you are looking to query more about the EC2 instances 

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/examples.html

* Check out the Azure python SDK link if link if you are looking to query more about the Azure instances.

This project is leveraging these versions of the Azure python libraries. 

azure-common==1.1.27
azure-core==1.13.0
azure-identity==1.5.0
azure-mgmt-compute==20.0.0
azure-mgmt-core==1.2.2
azure-mgmt-network==18.0.0

https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-overview

https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-example-list-resource-groups

https://pypi.org/project/azure-mgmt-compute/

https://pypi.org/project/azure-mgmt-network/


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
