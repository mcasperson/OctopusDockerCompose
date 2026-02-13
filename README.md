A Docker compose stack that uses the latest Octopus Docker image and installs a bunch of common tools on top including:

* Python
* PowerShell
* Terraform
* Kubectl
* Azure CLI

To start the stack, run `start.sh`.

To capture network traffic, run mitmproxy, and start octopus with `./start.sh 172.17.0.1:8080`