
import requests

import time

def send_to_telegram(message):

    apiToken = '5652381810:AAFKaEVHXV81LekSo4lzHOxxKWLhI02qek8'
    chatID = '<id>'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

while True:
    send_to_telegram("<sfd>")
    time.sleep(1)
