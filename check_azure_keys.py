import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

def check_azure_key(key_env_var):
    key = os.getenv(key_env_var)
    endpoint = os.getenv("AZURE_ENDPOINT")
    region = os.getenv("AZURE_REGION")

    print(f"{key_env_var} = {key}")

    if not key or not endpoint or not region:
        print(f"Missing required environment variable(s) for {key_env_var}")
        return

    url = f"{endpoint}translate?api-version=3.0&to=es"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json"
    }
    body = [{"Text": "test"}]

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            print(f"{key_env_var} is working.\n")
        else:
            print(f"{key_env_var} gave status {response.status_code}: {response.json()}\n")
    except Exception as e:
        print(f"Error accessing {key_env_var}: {e}\n")

if __name__ == "__main__":
    check_azure_key("AZURE_KEY_1")
    check_azure_key("AZURE_KEY_2")

