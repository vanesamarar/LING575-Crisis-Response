# LING575-Crisis-Response

This project evaluates the performance of Google Translate and Microsoft Translator in translating emergency weather alerts issued by the U.S. National Weather Service (NWS). The goal is to assess machine translation quality in both forward (English → target language) and backward (target language → English) directions across five high-priority languages: Spanish, Somali, Khmer, Korean, and Vietnamese.

# Authors 

Melody Bechler & Vanesa Marar


Data is compiled from the National Weather Service (NWS) Product Translations, NWS Tsunami Products, and National Hurricane Center and Central Pacific Hurricane Center's Advisory Archive. NWS provides limited historical English alerts for a finite number of NWS stations in the United States and the National Hurricane Center has advisory archives dating from 1998. 


## Setup

In order to run the pipeline, you need to complete the following 3 steps:
1. Configure environmental variables
2. Create Google Cloud account and get API key
3. Create Azure account and get API key and endpoint

Configure your API credentials in a .env file. If you are only using one API key per provider, modify the relevant scripts accordingly (e.g., removing {key}_2 from .env and translation scripts outlined below):

```bash
$ GOOGLE_APPLICATION_CREDENTIALS_1=""
$ GOOGLE_APPLICATION_CREDENTIALS_2=""
$ AZURE_KEY_1=""
$ AZURE_KEY_2=""
$ AZURE_ENDPOINT=""
```


### Google Setup
Google Cloud Translation can be accessed via Google.

1. Create free account (https://cloud.google.com/?hl=en)
2. Enable Cloud Translation API
3. Create a service account in IAM
4. Grant service account permission to use translation API 
5. Create and download a JSON key
6. Add key to .env file and store json key with other files
7. Download gcloud CLI (https://cloud.google.com/sdk/gcloud)
8. Run 'gcloud init'
9. Run 'pip install --upgrade google-cloud-translate'

* I think this is right...

### Azure

Azure AI Translator can be accessed via the Azure platform.

1. Create a free Azure account (https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account)
2. Create a single service resource. Location 'westus2' was chosen.
3. Navigate to Keys and Endpoint page and copy your endpoint and key. If an endpoint is not listed, use "https://api.cognitive.microsofttranslator.com".
4. Add keys and endpoint to .env
5. Run 'pip install requests uuid'


Your .gitignore file should list your json file(s) and your .env file. If only using a single API key for both Azure and Google Cloud, you can change the 'AZURE_KEY_2' and "GOOGLE_APPLICATION_CREDENTIALS_2' in the azure_backtranslation.py and google_cloud_backtranslation.py scripts to reflect the single key, as 'AZURE_KEY_1' and 'GOOGLE_APPLICATION_CREDENTIALS_1'. If only using a single API credentials in each (compared to our two sets), you must change the scripts below to reflect the single key set. 

**Anything else to add to these?

### Running the Pipeline
Run the following command to execute the full pipeline:
```bash
python3 pipeline.sh
```
This will call the scripts outlined in the next section in the order they are presented.
Please ensure the above Google Cloud and Azure API credentials are correct prior to running.

### Scripts
```bash
1. azure_translation.py
```
This script translates English text into the 5 target languages (forward translation) using the Azure Translator.

```bash
2. google_translation.py
```
This script translates English text into the 5 target languages (forward translation) using the Neural Machine Translation in Google Cloud Translation API. 

```bash
3. forward_evaluation.py
```
This script evaluates the forward translations produced by the first two scripts using Comet-Kiwi and MonoTransQuest.

```bash
4. azure_backtranslation.py
```
This script translates the first script's output from the 5 languages back into English (back-translation) using the Azure Translator.

```bash
5. google_backtranslation.py
```
This script translates the second script's output from the 5 languages back into English (back-translation) using Neural Machine Translation in Google Cloud Translation API.

```bash
6. back_evaluation.py
```
This script evaluates the back-translations produced by scripts 4 and 5 using Comet, BLEU, and BERTScore.



### Evaluation --- add MORE info here about implementation
Run the following commands in the terminal to install the required evaluation packages. This process assumes conda is already installed. To download conda, download here: (https://www.anaconda.com/docs/getting-started/anaconda/main)


### Requirements
Install dependencies with:
```bash
'pip install python-dotenv'
'conda install -c huggingface transformers=4.6.1'
'pip install "unbabel-comet>=2.0.0" '
'pip install transquest'
'pip install simpletransformers'
'pip install bert-score'
```
We used the HuggingFace Transformers 4.6.1 version within a Conda environment named hf46 using python version 3.8.




