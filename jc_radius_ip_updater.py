#!/usr/bin/env python3
import json
import socket
import requests

## Global variables
# Configuration
config_file = 'jc_radius.conf'
config = {}

# Sites information (bare identifiers, ips, and other things)
info_base = {
    "id": None,
    "name": None,
    "domain": None,
    "oldIP": None,
    "newIP": None
}
sites_info = []
radius_info = []

## Try reading the config file (JSON)
try:
    with open(config_file) as conf:
        config = json.load(conf)
except:
    exit("Error:\t missing or invalid configuration file")
    
## Set some more variables to get us going... No error checking for now :(
api_key = config["apiKey"]

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

## Dynamic IP Adress retriever
def get_dynamic_ip(domain): 
    try: 
        return socket.gethostbyname(domain) 
    except: 
        return None
    
## IP Address Updater
def update_ip(id, ip):
    # Make an API Call
    url = 'https://console.jumpcloud.com/api/radiusservers/{}'.format(id)
    result = jc_api_call('put', url, data = {"networkSourceIp": ip})
    
    ## Remember, it's json!
    return result

## Initializer
def init():
    ## Reference some globals
    global sites_info, radius_info
    
    ## Add the site information from config
    for site in config["sites"]:
        info = info_base.copy()
        info["name"] = site["name"]
        info["domain"] = site["domain"]
        sites_info.append(info)
    
    ## Get the radius server information
    radius_info = jc_api_call('get', 'https://console.jumpcloud.com/api/radiusservers/')["results"]
    
    ## Check our config with what JC has on file
    for site in sites_info:
        # We will use this in a sec
        site_name = site["name"]
        domain = site["domain"]
        
        # For every JC site
        for radius_item in radius_info:
            # Is our site in JC?
            if site_name == radius_item["name"]:
                # Set the ID for that site
                site["id"] = radius_item["id"]
                
                # Set the current JC IP for that site
                site["oldIP"] = radius_item["networkSourceIp"]
            
## The Status Checker
def check_status():
    # For every site of OURS
    for site in sites_info:
        # IP's to compare
        oldIP = site["oldIP"]
        currentIP = get_dynamic_ip(site["domain"])
        
        # Check if the IP has changed
        if oldIP != currentIP:
            # Let the user know!
            print("The IP address {} is not current for {}".format(oldIP, site["name"]))
            
            # Change the IP :)
            site["newIP"] = currentIP
            update_ip(site["id"], currentIP)
        else:
            print("No changes for {}".format(site["name"]))
            site["newIP"] = oldIP # For finalization()
     
## Finalization function, updates config with new ID's, etc...
def finalize():
    # Global references
    global config
    
    # Copy the config, (original will be backed up)
    new_config = config.copy()
    
    # Iterate over every site of ours
    for site in sites_info: # Could check None keys and only write that way if user was ahead/advanced :)
        # We will use this in a sec
        ID = site["id"]
        name = site["name"]
        last_ip = site["newIP"]
        
        # Write mem config changes
        for x in new_config["sites"]:
            if x["name"] == name:
                # The index of x!!!
                index = new_config["sites"].index(x)
                
                # The ID, if applicable
                new_config["sites"][index]["id"] = ID
                new_config["sites"][index]["last_ip"] = last_ip
        
    # Create a backup of old config
    with open('{}.bak'.format(config_file), 'w') as outfile:
        json.dump(config, outfile)
    
    # Write the new config file
    with open(config_file, 'w') as outfile:
        json.dump(new_config, outfile, indent=4)

## The main function
def main():
    # Initialize
    init()
    
    # Check the statuses, change IPs if necessary
    check_status()
   
    # Finalize
    finalize()

## Main function/method
if __name__ == "__main__":
    main()
