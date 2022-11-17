import requests
import os
import json

installsURL = "https://api.wpengineapi.com/v1/installs?limit=10"

sitesURL = "https://api.wpengineapi.com/v1/sites?limit=10"

backupjson = {
    "description": "Updates Backup",
    "notification_emails": [
        "jesse@csdesignstudios.com"
    ]
}

# API Keys
# 0c27ac7e-b74d-4e8d-b469-a9304b4e3368 : zzc4M8UuAh49S7vjREYMa1O58vLliESl
response = requests.get(sitesURL,
    auth=requests.auth.HTTPBasicAuth(
    '0c27ac7e-b74d-4e8d-b469-a9304b4e3368',
    'zzc4M8UuAh49S7vjREYMa1O58vLliESl'))

j = response.json()
envName = 'loantucson'
#envId = j['results'][0][envName]['id']
print(j)

#print(response.text)

def run_backup(envId):
    
    requests.post('https://api.wpengineapi.com/v1/installs/' + envId + '/backups', json = myobj)