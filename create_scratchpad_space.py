#!/usr/bin/env python3
import json
import os

import requests
import uuid

def get_octopus_resource(uri):
    response = requests.get(uri, headers=headers)
    response.raise_for_status()

    return json.loads(response.content.decode('utf-8'))

def get_by_name(uri, name):
    resources = get_octopus_resource(uri)
    return next((x for x in resources if x['Name'] == name), None)

# Define Octopus server variables
octopus_server_uri = 'http://localhost:8083'
octopus_api_key = 'API-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
headers = {'X-Octopus-ApiKey': octopus_api_key}

# Define working variables
space_name = "Scratchpad2"
space_description = "Test space"
managers_teams = ["teams-managers"] # Either this or manager_team_members must be populated otherwise you'll receive a 400
manager_team_members = [] # Either this or managers_teams must be populated otherwise you'll receive a 400

try:
    space = get_by_name('{0}/api/spaces/all'.format(octopus_server_uri), space_name)
    if space:
        space['TaskQueueStopped'] = True

        # update task queue to stopped
        uri = '{0}/api/spaces/{1}'.format(octopus_server_uri, space['Id'])
        response = requests.put(uri, headers=headers, json=space)
        response.raise_for_status()

        # Delete space
        response = requests.delete(uri, headers=headers)
        response.raise_for_status()
except Exception as e:
    print(e)
    if response:
        print(response.text)
    pass

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
uri = '{0}/api/spaces'.format(octopus_server_uri)
response = requests.post(uri, headers=headers, json=space)
print(response.text)
response.raise_for_status()

# Create the worker pool
# uri = '{0}/api/{1}/workerpools'.format(octopus_server_uri, response.json()['Id'])
# worker_pool = {
#     "Name":"Hosted Ubuntu",
#     "Description":"",
#     "SortOrder":-1,
#     "IsDefault":False,
#     "CanAddWorkers":False,
#     "WorkerPoolType":"StaticWorkerPool"
# }
# response = requests.post(uri, headers=headers, json=worker_pool)
# response.raise_for_status()
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