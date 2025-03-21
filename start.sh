#!/bin/bash

pushd server

docker compose up -d

# Create the Octopus database
docker compose exec mssql sh -c '/opt/mssql-tools18/bin/sqlcmd -C -S localhost -U SA -P Password01! -Q "CREATE DATABASE Octopus;"'

# Install all the tools we'll need to perform deployments
docker compose exec octopus sh -c 'curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs'
docker compose exec octopus sh -c 'apt-get install -y jq git dnsutils zip gnupg software-properties-common python3 python3-pip'
docker compose exec octopus sh -c 'pip install slack_sdk'
docker compose exec octopus sh -c 'pip install pycryptodome'
docker compose exec octopus sh -c 'apt update; apt install -y --no-install-recommends gnupg curl ca-certificates apt-transport-https && curl -sSfL https://apt.octopus.com/public.key | apt-key add - && sh -c "echo deb https://apt.octopus.com/ stable main > /etc/apt/sources.list.d/octopus.com.list" && apt update; apt install -y octopuscli'
docker compose exec octopus sh -c 'wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor > /usr/share/keyrings/hashicorp-archive-keyring.gpg'
docker compose exec octopus sh -c 'echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" > /etc/apt/sources.list.d/hashicorp.list'
docker compose exec octopus sh -c 'apt update --allow-insecure-repositories; apt-get install -y terraform'
docker compose exec octopus sh -c 'curl -sL https://aka.ms/InstallAzureCLIDeb | bash'
docker compose exec octopus sh -c 'if [ ! -f /usr/local/bin/kubectl ]; then curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"; install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl; fi'
docker compose exec octopus sh -c 'RELEASES=$(curl --silent https://api.github.com/repos/OctopusDeployLabs/terraform-provider-octopusdeploy/releases | jq -r ".[] | .name[1:]"); echo $RELEASES; for RELEASE in ${RELEASES}; do echo "Downloading https://github.com/OctopusDeployLabs/terraform-provider-octopusdeploy/releases/download/v${RELEASE}/terraform-provider-octopusdeploy_${RELEASE}_linux_amd64.zip"; mkdir -p "/terraformcache/registry.terraform.io/octopusdeploylabs/octopusdeploy/${RELEASE}/linux_amd64"; cd "/terraformcache/registry.terraform.io/octopusdeploylabs/octopusdeploy/${RELEASE}/linux_amd64"; if [ ! -f "terraform-provider-octopusdeploy_v${RELEASE}" ]; then curl --silent -L -o "terraform-provider-octopusdeploy_${RELEASE}_linux_amd64.zip" "https://github.com/OctopusDeployLabs/terraform-provider-octopusdeploy/releases/download/v${RELEASE}/terraform-provider-octopusdeploy_${RELEASE}_linux_amd64.zip"; unzip "terraform-provider-octopusdeploy_${RELEASE}_linux_amd64.zip"; rm "terraform-provider-octopusdeploy_${RELEASE}_linux_amd64.zip"; fi; done'
# https://developer.hashicorp.com/terraform/cli/config/config-file#explicit-installation-method-configuration
docker compose exec octopus sh -c 'echo "provider_installation {\nfilesystem_mirror {\npath = \"/terraformcache\"\ninclude = [\"registry.terraform.io/octopusdeploylabs/octopusdeploy\"]\n}direct {\nexclude = [\"registry.terraform.io/octopusdeploylabs/octopusdeploy\"]\n}\n}" > ~/.terraformrc'
docker compose exec octopus sh -c 'curl https://packages.microsoft.com/keys/microsoft.asc | gpg --yes --dearmor --output /usr/share/keyrings/microsoft.gpg'
docker compose exec octopus sh -c 'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/microsoft-debian-bullseye-prod bullseye main" > /etc/apt/sources.list.d/microsoft.list'
docker compose exec octopus sh -c 'apt update --allow-insecure-repositories && apt install -y powershell'

popd