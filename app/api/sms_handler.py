import requests

sms_api_url = 'https://textbelt.com/text'
sms_api_key = 'textbelt'


# Sends a message to a number with a message
def send_mock_sms(message, number):
    resp = requests.post(sms_api_url, {
        'phone': number,
        'message': message,
        'key': sms_api_key,
    })
    json_response = resp.json()
    return json_response['success']


# Sends a message to a number after a vaccination has taken place
def send_mock_vaccination_sms(message, number, unique_id):
    message = message + " your unique ID is: " + unique_id
    resp = requests.post(sms_api_url, {
        'phone': number,
        'message': message,
        'key': sms_api_key,
    })
    json_response = resp.json()
    return json_response['success']
