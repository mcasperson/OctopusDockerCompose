#!/usr/bin/env python3
import json
import os

import requests
import uuid

# Define Octopus server variables
octopus_server_uri = os.getenv("OCTOPUS_CLI_SERVER")
octopus_api_key = os.getenv("OCTOPUS_CLI_API_KEY")
headers = {'X-Octopus-ApiKey': octopus_api_key}

# Define working variables
space_name = "AI"

# Create the space
uri = '{0}/api/spaces'.format(octopus_server_uri)
spaces = requests.get(uri, headers=headers)

space = next(space for space in spaces.json()["Items"] if space['Name'] == space_name)

if space:
    space_id = space['Id']
    # Get all projects in the space
    tenants_uri = f"{octopus_server_uri}/api/{space_id}/tenants"
    tenants = requests.get(tenants_uri, headers=headers).json()["Items"]

    # Delete all projects
    for tenant in tenants:
        tenant_id = tenant['Id']
        delete_uri = f"{octopus_server_uri}/api/{space_id}/tenants/{tenant_id}"
        response = requests.delete(delete_uri, headers=headers)
        print(f"Deleted tenant {tenant['Name']}: {response.status_code}")
else:
    print("Space not found.")