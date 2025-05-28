# LING575-Crisis-Response

This project evaluates Google Translate and Microsoft Translate's ability to effectively translate National Weather Service  alerts from English into Somali, Vietnamese, Khmer, Korean, and Spanish, as well as translating back to English.


Data is compiled from the National Weather Service (NWS) Product Translations, NWS Tsunami Products, and National Hurricane Center and Central Pacific Hurricane Center's Advisory Archive. NWS provides limited historical English alerts for a finite number of NWS stations in the United States and the National Hurricane Center has advisory archives dating from 1998. 


## Setup

In order to run any translators, you need to configure environmental variables. You will also need to create Google Cloud and Azure accounts, then create API keys for each. Azure requires an endpoint. The Azure and Google API keys can be the same. For the purpose of this project, we each have individual API keys, therefore we needed to set up two sets of credentials for each platform.

'''
GOOGLE_APPLICATION_CREDENTIALS_1=""
GOOGLE_APPLICATION_CREDENTIALS_2=""
AZURE_KEY_1=""
AZURE_KEY_2=""
AZURE_ENDPOINT=""
'''

### Google Setup
Google Cloud Translation can be accessed via Google.

1. Create free account (https://cloud.google.com/?hl=en)
2. Ensure the Cloud Translation API is enabled for the project
3. Go to IAM in search bar and create new Service Account
4. Grant service account access to use translation API 
5. Go to keys and create new json key
6. Add key to .env file and store json key with other files
7. Download gcloud CLI (https://cloud.google.com/sdk/gcloud)
8. Run 'gcloud init'
9. Run 'pip install --upgrade google-cloud-translate'

* I think this is right...

### Azure

Azure AI Translator can be accessed via the Azure platform.

1. Create a free Azure account ()
2. Create a single service resource in the Azure portal. Location 'westus2' was chose. The key and endpoint are on the Keys and Endpoint page. If no endpoint listed, use "https://api.cognitive.microsofttranslator.com".
3. Add keys and endpoint to .env
4. Run 'pip install requests uuid'
5. Store keys and endpoint in .env

**Anything else to add to these?

