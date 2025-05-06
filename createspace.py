#!/usr/bin/env python3
import json
import requests
import uuid

# Define Octopus server variables
octopus_server_uri = 'http://localhost:8083/api'
octopus_api_key = 'API-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
headers = {'X-Octopus-ApiKey': octopus_api_key}

# Define working variables
space_name = str(uuid.uuid4()).replace("-", "")[:20]
space_description = "Test space"
managers_teams = ["teams-administrators"] # Either this or manager_team_members must be populated otherwise you'll receive a 400
manager_team_members = [] # Either this or managers_teams must be populated otherwise you'll receive a 400

# Define space JSON
space = {
    'Name' : space_name,
    'Description' : space_description,
    'SpaceManagersTeams' : managers_teams,
    'SpaceManagersTeamMembers' : manager_team_members,
    'IsDefault' : False,
    'TaskQueueStopped' : False
}

# Create the space
uri = '{0}/spaces'.format(octopus_server_uri)
response = requests.post(uri, headers=headers, json=space)
print(response.text)
response.raise_for_status()

# Create the worker pool
uri = '{0}/{1}/workerpools'.format(octopus_server_uri, response.json()['Id'])
worker_pool = {
    "Name":"Hosted Ubuntu",
    "Description":"",
    "SortOrder":-1,
    "IsDefault":False,
    "CanAddWorkers":False,
    "WorkerPoolType":"StaticWorkerPool"
}
response = requests.post(uri, headers=headers, json=worker_pool)
response.raise_for_status()
#
# worker_pool = {
#     "Name":"Hosted Windows",
#     "Description":"",
#     "SortOrder":-1,
#     "IsDefault":False,
#     "CanAddWorkers":False,
#     "WorkerPoolType":"StaticWorkerPool"
# }
# response = requests.post(uri, headers=headers, json=worker_pool)
# response.raise_for_status()


print(space_name)