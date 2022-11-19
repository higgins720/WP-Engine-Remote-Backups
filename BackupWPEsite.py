import requests
import os.path
import json

backupName = 'wisdomecare'

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

# Get a list of all environments in the system
# Rather than compiling a list every time, reference json file if it exists, if not then write one.
if (os.path.exists('installs.json')):
    # fill dictionary with json file data
    with open('installs.json') as json_file:
        jsonFile = json.load(json_file)
        #print("JSON results: " + str(len(object["results"])))
        print("Loading Installs...")
        for key, value in jsonFile.items():
            nameRecordDictionary[key] = value
else:
    print("Compiling list of environments...")
    nextURL = 'https://api.wpengineapi.com/v1/installs'
    while nextURL is not None:
        installsResponse = requests.get(nextURL, auth=requests.auth.HTTPBasicAuth(apiKey[0], apiKey [1]), timeout=10)
        object = json.loads(installsResponse.text)
        print("HTTP results: " + str(len(object["results"])))
        nextURL = object["next"]
        print(object["count"])
        print(object["next"])
    
        for record in object["results"]:
            nameRecordDictionary[record["name"]] = record

        with open('installs.json', 'w', encoding='utf-8') as f:
            json.dump(nameRecordDictionary, f)

# Now that we know the dictionary is populated, we can store values
installID = nameRecordDictionary[backupName]["id"]

def run_backup(install_ID, name):
    # 'https://api.wpengineapi.com/v1/installs'
    backupURL = 'https://api.wpengineapi.com/v1/installs/' + install_ID + '/backups'
    #print(backupURL)
    data = {"description": "Taking a backup of " + name, "notification_emails": ["jesse@csdesignstudios.com"]}
    backupResponse = requests.post(backupURL, auth=requests.auth.HTTPBasicAuth(apiKey[0], apiKey[1]), timeout=100, json=data)
    print(backupResponse.text)
    object = json.loads(backupResponse.text)
    #print(object["id"])
    return object["id"]

# This just returns the phrase "Requested"
def backup_status(install_ID, backup_ID):
    backupStatusURL = 'https://api.wpengineapi.com/v1/installs/' + install_ID + '/backups/' + backup_ID
    print(backupStatusURL)
    backupStatusResponse = requests.get(backupStatusURL, auth=requests.auth.HTTPBasicAuth(apiKey[0], apiKey[1]), timeout=10)
    print(backupStatusResponse.text)

backupID = run_backup(installID, backupName)
#backup_status(installID, backupID)