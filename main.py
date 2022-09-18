import os
import yaml
import github
import requests

api_name = os.environ["INPUT_API_NAME"]
api_owner = os.environ["INPUT_API_OWNER"]
api_spec_file_path = os.environ["INPUT_API_SPEC_FILE_PATH"]
swaggerhub_api_key = os.environ["INPUT_SWAGGERHUB_API_KEY"]

endpoint = f"https://api.swaggerhub.com/apis/{api_owner}/{api_name}"

with open(api_spec_file_path) as f:
    api_spec = yaml.safe_load(f)

API_VERSION = api_spec["info"]["version"]
print(f"Uploading API spec with version {API_VERSION}...")

# Upload new api spec
try:
    r = requests.post(
        f"{endpoint}?vrsion={API_VERSION}",
        headers={
            "authorization": swaggerhub_api_key,
            "content-type": "application/yaml",
        },
        data=api_spec,
    )
    r.raise_for_status()
except Exception as error:
    print(r.json())
    raise

print(f"Changing default version of the API spec to {API_VERSION}...")

# Change api spec default version to the new one
default_version = {"version": str(API_VERSION)}
try:
    r = requests.put(
        f"{endpoint}/settings/default",
        headers={
            "authorization": swaggerhub_api_key,
            "content-type": "application/json",
        },
        json=default_version,
    )
    r.raise_for_status()
except Exception as error:
    print(r.json())
    raise

print("Updating API spec successful.")
