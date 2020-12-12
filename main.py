import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
base_api_url = 'https://semsportal.com/api/'


def get_session_token():
    login_payload = {
        'account': os.getenv('GOODWE_USERNAME'),
        'pwd': os.getenv('GOODWE_PASSWORD')
    }
    login_headers = {
        'User-Agent': 'PVMaster/2.0.4 (iPhone; iOS 11.4.1; Scale/2.00)',
        'Token': '{"version": "v2.0.4", "client": "ios", "language": "en"}'
    }

    login_response = requests.post(base_api_url + 'v2/Common/CrossLogin',
                                   headers=login_headers,
                                   data=login_payload,
                                   timeout=10,
                                   )

    login_response.raise_for_status()
    login_data = login_response.json()
    token = json.dumps(login_data['data'])

    return token


def get_power_flow(token):
    headers = {
        'User-Agent': 'PVMaster/2.0.4 (iPhone; iOS 11.4.1; Scale/2.00)',
        'Token': token
    }
    payload = {
        'powerStationId': os.getenv('GOODWE_SYSTEMID')
    }

    response = requests.post(base_api_url + 'v2/PowerStation/GetPowerflow',
                             headers=headers,
                             data=payload,
                             timeout=10,
                             )

    response.raise_for_status()
    data = response.json()
    return data['data']['pv'] if data else ""


if __name__ == '__main__':
    session_token = get_session_token()
    pv = get_power_flow(session_token)
    print(pv or "zZz")

