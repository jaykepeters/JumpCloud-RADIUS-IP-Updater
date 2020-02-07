# JumpCloud-RADIUS-IP-Updater

# Installation
1. Move the script into /usr/local/bin with proper permissions
2. Create a configuration file: see below for syntax
3. Add to your crontab on unifi controller, run every hour. 

# Configuration
The bare minimum config file should look like this:
```json
{
  "apiKey": "YOUR API KEY",
  "networks": {
    "RADIUS SERVER NAME": {
      "domain": "dynamic dns domain",
      `Optionals`
      "site ID": "if you know the id, otherwise script will ad to make faster",
      "last_ip": "ip recorded on last run of the script"
  }
}
```

# Usage
Everything is done by the script! More functionality may be added later if felt needed
