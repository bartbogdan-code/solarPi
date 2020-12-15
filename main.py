import os
import json
import requests
import time
from dotenv import load_dotenv

try:
    import smbus
    from microdotphat import write_string, clear, show

    i2c_present = True
except ImportError as e:
    i2c_present = False
    pass

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

    try:
        login_response = requests.post(base_api_url + 'v2/Common/CrossLogin',
                                       headers=login_headers,
                                       data=login_payload,
                                       timeout=10,
                                       )
        login_response.raise_for_status()
        login_data = login_response.json()
        token = json.dumps(login_data['data'])
        return True, token
    except requests.exceptions.HTTPError as token_exception:
        return False, str(token_exception.response.status_code)


def get_power_flow(token):
    headers = {
        'User-Agent': 'PVMaster/2.0.4 (iPhone; iOS 11.4.1; Scale/2.00)',
        'Token': token
    }
    payload = {
        'powerStationId': os.getenv('GOODWE_SYSTEMID')
    }
    try:
        response = requests.post(base_api_url + 'v2/PowerStation/GetPowerflow',
                                 headers=headers,
                                 data=payload,
                                 timeout=10,
                                 )

        response.raise_for_status()
        data = response.json()
        if data['data']['pv'].endswith('(W)'):
            pv = data['data']['pv'][:-3]
        else:
            pv = data['data']['pv']
        return True, pv
    except requests.exceptions.HTTPError as data_exception:
        return False, str(data_exception.response.status_code)


def write_to_display(message):
    if i2c_present:
        clear()
        write_string(message, kerning=False)
        show()
    print(message)


def main():
    pv_success = False
    while True:
        if not pv_success:
            # Get new token
            token_success, token_value = get_session_token()

        if token_success:
            pv_success, pv_value = get_power_flow(token_value)
            if pv_success:
                message = pv_value or "zZz"
            else:
                message = "DE:" + pv_value
        else:
            message = "TE:" + token_value

        write_to_display(message)

        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
