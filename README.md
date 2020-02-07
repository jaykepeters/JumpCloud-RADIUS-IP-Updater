# JumpCloud-RADIUS-IP-Updater

# Installation
1. Move the script into `/usr/local/bin` like this:
```bash
cd /usr/local/bin
wget https://raw.githubusercontent.com/jaykepeters/JumpCloud-RADIUS-IP-Updater/master/jc_radius_ip_updater.py
mv jc_radius_ip_updater.py radupdate
chmod a+x radupdate
```
2. Create a configuration file and initial log (see below)
3. Add a cron entry to run this script at a desired interval. I recommend running the script every 15 minutes.:
`nano /etc/crontab`
Append the following entry (assuming the path is set):
`0 *     * * *   root    radupdate > /var/log/radupdate.log 2>&1`
You may want to also reload cron just to be safe and sure:
`service cron reload`

# Configuration
This is what your configuration file should look like:
```json
{
    "apiKey": "YOUR API KEY",
    "sites": [
        {
            "name": "RADIUS SERVER NAME",
            "domain": "DOMAIN ASSOCIATED WITH ROUTER's PUBLIC DHCP IP",
            "id": "IF YOU KNOW IT, SCRIPT FINDS TOO :)",
            "last_ip": "IF YOU KNOW IT, SCRIPT RE-REWRITES IP to file"
        }
    ]
}
```
The `id` and `last_ip` keys are optional. The script will rewrite your configuration file with these keys if they are not already set on every run.

Save something like this to `/etc/jc_radius.conf` or another name/path of your choosing. Inside the script, you must also update the `conf_file` variable with the path of this config file. Failure to follow these steps will result in a runtime error. 

To enable logging to work correctly with the given cron entry, you must first initialize the log file:
`touch /var/log/radupdate.log`

In the event that your configuration file is corrupted after running this script, check for the existence of a `{CONFIG FILENAME}.bak` file in the same directory as your original configuration file. 

# Usage
1. Cron will run the script every x minutes, **OR**
2. Run the script like so: `radupdate`

# Support
In the event that you need help using this product, please feel free to open up an issue and I will respond promptly!

# Development
There are a few features that could be added in the future for ease of simplicity and to make the user feel even more lazy:
- [ ] More error checking, more verbosity
- [ ] Command line interface to add, update, and delete RADIUS entries
- [ ] Logging implementation that is not in cron and bash
