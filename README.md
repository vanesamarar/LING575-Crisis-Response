# LING575-Crisis-Response

This project evaluates Google Translate's (and Microsoft Translator) ability to effectively translate weather alerts from English into other languages, as well as backtranslations to English.


Data is compiled from the National Weather Service (NWS) Product Translations, NWS Tsunami Products, and National Hurricane Center and Central Pacific Hurricane Center's Advisory Archive. NWS provides limited historical English alerts for a finite number of NWS stations in the United States and the National Hurricane Center has advisory archives dating from 1998. 


## Setup

In order to run any translators, you need to configure environmental variables. You will also need to create Google Cloud and Azure accounts, then create API keys for each. Azure requires an endpoint. The Azure and Google API keys can be the same. For the purpose of this project, we each have individual API keys, therefore we needed to set up two sets of credentials for each platform.

GOOGLE_APPLICATION_CREDENTIALS_1=""
GOOGLE_APPLICATION_CREDENTIALS_2=""
AZURE_KEY_1=""
AZURE_KEY_2=""
AZURE_ENDPOINT=""
