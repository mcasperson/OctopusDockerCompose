#!/usr/bin/env python3
import json
import requests
import uuid

# Define Octopus server variables
octopus_server_uri = 'http://localhost:8083/api'
octopus_api_key = 'API-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
headers = {'X-Octopus-ApiKey': octopus_api_key}

# Define working variables
space_name = "Test Space"
space_description = "Test space"
managers_teams = ["teams-administrators"] # Either this or manager_team_members must be populated otherwise you'll receive a 400
manager_team_members = [] # Either this or managers_teams must be populated otherwise you'll receive a 400

# Create the space
uri = '{0}/spaces'.format(octopus_server_uri)
spaces = requests.get(uri, headers=headers)

space_id = [space['Id'] for space in spaces.json()["Items"] if space['Name'] == space_name]

if space_id:
    stop_queue = {'TaskQueueStopped': True}
    uri = '{0}/spaces/{1}'.format(octopus_server_uri, space_id)
    print(uri)
    response = requests.put(uri, headers=headers, json=stop_queue)
    response.raise_for_status()

    response = requests.delete(uri, headers=headers)
    print(response.text)
    response.raise_for_status()