#!/usr/bin/env python3
import json
import requests

## Global variables
config_file = 'jc_radius.conf'
config = {}
my_servers = {}

## Try reading the config file (JSON)
try:
    with open(config_file) as conf:
        config = json.load(conf)
except:
    exit("Error:\t missing or invalid configuration file")
    
## Set some more variables to get us going... No error checking for now :(
api_key = config["apiKey"]
radius_server_names = config["networks"].keys()

## Standard JumpCloud API Call
def jc_api_call(method, url, additional_headers={}, data=None):
    # Headers!
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    headers.update(additional_headers)
    
    # Arguments to pass to requests
    core_arguments = [method.lower(), url]
    
    # Additional arguments
    aa = {
        "headers": headers,
        "data": None
    }
    
    # Is there any data?
    if data is not None:
        aa["data"] = json.dumps(data)
        
    # Make the request, store as response
    response = requests.request(*core_arguments, headers=aa["headers"], data=aa["data"])
    
    # Return a dict of response data
    return response.json()

## IP Address Updater
def update_ip(id, ip):
    # Make an API Call
    url = 'https://console.jumpcloud.com/api/radiusservers/{}'.format(id)
    result = jc_api_call('put', url, data = {"networkSourceIp": ip})
    
    ## Remember, it's json!
    return result

## The main function
def main():
    # Test update IP
    print(update_ip('5c8b65508443f917b712b90b', '2.24.6.18'))

## Main function/method
if __name__ == "__main__":
    main()
    
## Edit the config with ids to make things faster on subsequent runs... pass name and done!
