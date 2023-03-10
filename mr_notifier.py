import time
import requests
import json
import datetime
import pync
import os
import logging

logging.basicConfig(level=logging.INFO)

home_dir = os.path.expanduser("~")
file_path = os.path.join(home_dir, ".config/mr_notifier.json")
try:
	with open(file_path, "r") as config_file:
		config_data = json.load(config_file)
except FileNotFoundError:
    print("Error: config.json file not found.")
except json.JSONDecodeError:
    print("Error: config.json file contains invalid JSON data.")
else:
    # Use the config_data variable here if the file was opened and parsed successfully
	logging.info("Successfully loaded config file.")
	GITLAB_HOST = config_data['gitlab_host']
	GITLAB_USER = config_data['gitlab_username']
	GITLAB_TOKEN = config_data['gitlab_access_token']
	INTERVAL = int(config_data['refresh_interval'])
	NOTIF_SOUND = config_data['notification_sound']

def notify(title, message, url, icon):
	pync.notify(title=title, message=message, open=url, sound=NOTIF_SOUND, icon=icon)

def api_call(config_data):
	try:	
		date=(datetime.datetime.utcnow() - datetime.timedelta(minutes=INTERVAL)).isoformat() + 'Z'
		url=f"https://{GITLAB_HOST}/api/v4/merge_requests?reviewer_username={GITLAB_USER}&state=opened&created_after={date}"
		headers={'PRIVATE-TOKEN':config_data['gitlab_access_token']}
		response=requests.get(url, headers=headers)
		logging.info(response.url)
		logging.debug(response.text)
		response.raise_for_status()
	except requests.exceptions.RequestException as ex:
		logging.error("API call failed with error: %s", ex)
	except ValueError as ex:
		logging.error("Failed to parse JSON response: %s", ex)
	return response.json()

try:
	while True:
		for mr in api_call(config_data):
			logging.debug(mr)
			notify(title='Merge Request', 
				message =f"{mr['author']['name']} has requested a review", 
				url=f'{mr["web_url"]}',
				icon=f'{mr["author"]["avatar_url"]}' #Currently icons do not work, but maybe someone can help make it work.
			) 
		time.sleep(INTERVAL*60)
except KeyboardInterrupt:
    print("Exiting...")
