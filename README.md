# LING575-Crisis-Response

This project evaluates the performance of Google Translate and Microsoft Translator in translating emergency weather alerts issued by the U.S. National Weather Service (NWS). The goal is to assess machine translation quality in both forward (English → target language) and backward (target language → English) directions across five high-priority languages: Spanish, Somali, Khmer, Korean, and Vietnamese.

# Authors 

Melody Bechler & Vanesa Marar


Data is compiled from the National Weather Service (NWS) Product Translations, NWS Tsunami Products, and National Hurricane Center and Central Pacific Hurricane Center's Advisory Archive. NWS provides limited historical English alerts for a finite number of NWS stations in the United States and the National Hurricane Center has advisory archives dating from 1998. 


## Setup

In order to run any translators, you need to configure environmental variables. You will also need to create Google Cloud and Azure accounts, then create API keys for each. Azure requires an endpoint. The Azure and Google API keys can be the same. For the purpose of this project, we each have individual API keys, therefore we needed to set up two sets of credentials for each platform.

Configure your API credentials in a .env file. If you are only using one API key per provider, modify the script accordingly (e.g., removing _2):

'''
GOOGLE_APPLICATION_CREDENTIALS_1=""
GOOGLE_APPLICATION_CREDENTIALS_2=""
AZURE_KEY_1=""
AZURE_KEY_2=""
AZURE_ENDPOINT=""
'''

GOOGLE_APPLICATION_CREDENTIALS_1=""
GOOGLE_APPLICATION_CREDENTIALS_2=""
AZURE_KEY_1=""
AZURE_KEY_2=""
AZURE_ENDPOINT=""

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

1. Create a free Azure account (https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account)
2. Create a single service resource in the Azure portal. Location 'westus2' was chosen. The key and endpoint are on the Keys and Endpoint page. If an endpoint is not listed, use "https://api.cognitive.microsofttranslator.com".
3. Add keys and endpoint to .env
4. Run 'pip install requests uuid'
5. Store keys and endpoint in .env

Your .gitignore file should list your json file(s) and your .env file. If only using a single API key for both Azure and Google Cloud, you can change the 'AZURE_KEY_2' and "GOOGLE_APPLICATION_CREDENTIALS_2' in the azure_backtranslation.py and google_cloud_backtranslation.py scripts to reflect the single key, as 'AZURE_KEY_1' and 'GOOGLE_APPLICATION_CREDENTIALS_1'. If only using a single API credentials in each (compared to our two sets), you must change the scripts below to reflect the single key set. 

**Anything else to add to these?

### Scripts
1. google_cloud_translation.py
This script translates English text (forward translation) using Neural Machine Translation in Google Cloud Translation API. Please ensure the above Google Cloud API credentials are correct prior to using.

2. azure_translate.py
This script translates English text (forward translation) using the Azure Translator. Please ensure the above Azure API credentials are correct prior to using.

3. google_cloud_backtranslation.py
This script translates text from 5 languages into English (backtranslation) using Neural Machine Translation in Google Cloud Translation API. Please ensure the above Google Cloud API credentials are correct prior to using.

4. azure_backtranslation.py
This script translates text from 5 languages into English (backtranslation) using the Azure Translator. Please ensure the above Azure API credentials are correct prior to using.


### Evaluation --- add MORE info here about implementation
Run the following commands in the terminal to install the required evaluation packages. This process assumes conda is already installed. To download conda, download here: (https://www.anaconda.com/docs/getting-started/anaconda/main)

The following downloads the dotenv module for to handle API keys, transformers 4.6.1, python 3.8, and hf46 environment:
'pip install python-dotenv'
'conda install -c huggingface transformers=4.6.1'
'pip install "unbabel-comet>=2.0.0" '
'pip install transquest'
'pip install simpletransformers'
'pip install bert-score'





