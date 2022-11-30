import requests
import os.path
import json
import time

backupName = 'flockf'
installsAddress = 'https://api.wpengineapi.com/v1/installs/'

nameRecordDictionary = {}
apiKey = []

# Check for API Keys
# Todo: have better security here
if (os.path.exists('keys.json')):
    with open('keys.json') as json_file:
        keysObject = json.load(json_file)
        for key, value in keysObject.items():
            apiKey.append(value)
else:
    # If no key file exists, write a new one with creds
    keyDict = {}
    key1 = input("Enter API Key 1/2: ")
    apiKey.append(key1)
    keyDict[0] = key1
    key2 = input("Enter API Key 2/2: ")
    apiKey.append(key2)
    keyDict[1] = key2
    with open('keys.json', 'w', encoding='utf-8') as key_file:
        json.dump(keyDict, key_file)

# Get a dictionary of all environments in the system
## Rather than compiling a list every time, reference json file if it exists, if not then write one.
if (os.path.exists('installs.json')):
    with open('installs.json') as json_file:
        jsonFile = json.load(json_file)
        for key, value in jsonFile.items():
            nameRecordDictionary[key] = value
else:
    print("Compiling list of environments...")
    nextURL = installsAddress
    while nextURL is not None:
        installsResponse = requests.get(nextURL, auth=requests.auth.HTTPBasicAuth(apiKey[0], apiKey[1]), timeout=10)
        object = json.loads(installsResponse.text)
        print("HTTP results: " + str(len(object["results"])))
        nextURL = object["next"]
        print(object["count"])
        print(object["next"])
    
        for record in object["results"]:
            nameRecordDictionary[record["name"]] = record

        with open('installs.json', 'w', encoding='utf-8') as f:
            json.dump(nameRecordDictionary, f)

installID = nameRecordDictionary[backupName]["id"]

def run_backup(install_ID, name):
    backupURL = installsAddress + install_ID + '/backups'
    data = {"description": "Taking a backup of " + name, "notification_emails": ["jesse@csdesignstudios.com"]}
    backupResponse = requests.post(backupURL, auth=requests.auth.HTTPBasicAuth(apiKey[0], apiKey[1]), timeout=100, json=data)
    object = json.loads(backupResponse.text)
    print(backupResponse.text)
    return object["id"]

def backup_status(install_ID, backup_ID):
    backupStatusURL = installsAddress + install_ID + '/backups/' + backup_ID
    backupStatusResponse = requests.get(backupStatusURL, auth=requests.auth.HTTPBasicAuth(apiKey[0], apiKey[1]), timeout=10)
    object = json.loads(backupStatusResponse.text)
    return object

# Runs a status check every couple of seconds until it returns as completed
def check_backup_status():
    while True:
        status = backup_status(installID, backupID)['status']
        checkSeconds = 5
        secondsElapsed = 0
        if (status != 'completed'):
            print('Backup ' + str(status) + '...')
            time.sleep(checkSeconds)
            secondsElapsed += checkSeconds
        elif (secondsElapsed == 60):
            print('Checks exceeded limit of 12; 60 seconds.')
            break
        else:
            print('Backup ' + str(status))
            break
        
backupID = run_backup(installID, backupName)
check_backup_status()