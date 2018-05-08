import requests  
import datetime
import json
from BotHandler import BotHandler

key = "577910923:AAG78ykB0qGRYEamF1rhSIp0PPhqwffaN18";
greet_bot = BotHandler(key)  
greetings = ('hello', 'hi', 'greetings', 'sup')  
now = datetime.datetime.now()


def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        webhook_url = "https://hooks.zapier.com/hooks/catch/2938864/fjb4tv/silent/" 
	
        if "#on" in last_chat_text:
            response = requests.post(
			    webhook_url, data=json.dumps({"text": last_chat_text.replace("#on", ""), "sender": last_chat_name}),
			    headers={'Content-Type': 'application/json'}
		    )
       
            if response.status_code != 200:
			    raise ValueError(
				    'Request to Zapier returned an error %s, the response is:\n%s'
				    % (response.status_code, response.text)
		    )
	
            elif response.status_code == 200:
			    print("pushed message from " + last_chat_name + ": " + last_chat_text)
		
        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
            today += 1
		
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()