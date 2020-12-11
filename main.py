import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = 'https://semsportal.com/api/'

payload = {
    'powerStationId': os.getenv('GOODWE_SYSTEMID')
}
login_payload = {
    'account': os.getenv('GOODWE_USERNAME'),
    'pwd': os.getenv('GOODWE_PASSWORD')
}

login_headers = {
    'User-Agent': 'PVMaster/2.0.4 (iPhone; iOS 11.4.1; Scale/2.00)',
    'Token': '{"version": "v2.0.4", "client": "ios", "language": "en"}'
}

login_response = requests.post(base_url + 'v2/Common/CrossLogin',
                               headers=login_headers,
                               data=login_payload,
                               timeout=10,
                               )

login_response.raise_for_status()
login_data = login_response.json()
token = json.dumps(login_data['data'])
headers = {
    'User-Agent': 'PVMaster/2.0.4 (iPhone; iOS 11.4.1; Scale/2.00)',
    'Token': token
}

response = requests.post(base_url + 'v2/PowerStation/GetPowerflow',
                         headers=headers,
                         data=payload,
                         timeout=10,
                         )
response.raise_for_status()
data = response.json()
print(data)

print(data['data']['pv'] or "ZzZ")
