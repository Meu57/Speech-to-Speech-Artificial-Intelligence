# SpeechtoSpeech-Artificial-Intelligence
#Deployment Process
I used the Azure terminal to initiate the deployment process.
First, I created a resource group named "Azurefunctionresource" using the following command:
az group create --name Azurefunctionresource --location Eastus
This step ensured that I had a dedicated resource group to manage my Azure resources.
Next, I created an Azure Storage Account named "ameenstorage" within the resource group. To achieve this, I executed the following command:
az storage account create --name ameenstorage --location Eastus --resource-group Azurefunctionresource --sku Standard_LRS
This allowed me to have a storage account in the East US region with the Standard LRS replication option.
After setting up the storage account, I proceeded to install the Azure Functions tools on my local machine. These tools provided the necessary command-line interface for managing and deploying Azure Functions.
With everything set up, I used the Azure Functions CLI (func) to deploy my function app named "ameenfunctionapp". I executed the following command:
func azure functionapp publish ameenfunctionapp --python
This command triggered the deployment process and published my function app to Azure using Python as the programming language.
By following these steps, I successfully deployed my Azure Function app, ensuring that it utilized the "ameenstorage" account located in the East US region.
