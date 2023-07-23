
from info import BOT_TOKEN
import requests

bot_token = BOT_TOKEN

def delete_bot_messages():
    get_updates_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(get_updates_url)
    data = response.json()

    for result in data['result']:
        chat_id = result['message']['chat']['id']
        message_id = result['message']['message_id']
        delete_message_url = f'https://api.telegram.org/bot{bot_token}/deleteMessage?chat_id={chat_id}&message_id={message_id}'
        requests.get(delete_message_url)

delete_bot_messages()

