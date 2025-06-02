import os

def test_credentials(env_var_name, label):
    path = os.getenv(env_var_name)
    if not path:
        print(f"{label} environment variable {env_var_name} not set.")
        return
    if os.path.isfile(path):
        print(f"{label} credentials file exists at: {path}")
    else:
        print(f"{label} credentials file NOT found at: {path}")

test_credentials("GOOGLE_APPLICATION_CREDENTIALS_1", "Forward translation key")
test_credentials("GOOGLE_APPLICATION_CREDENTIALS_2", "Backward translation key")

