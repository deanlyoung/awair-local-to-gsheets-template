# -*- coding: utf-8 -*-
#!/usr/bin/env python
import json
import requests
import httplib2
import os

from apiclient import discovery
from google.oauth2 import service_account
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

awair_url = ''

spreadsheet_id = ''
range_name = ''

secret_file = os.path.join(os.getcwd(), 'client_secret.json')
# secret_file = ''

sensors_list = []

def get_from_awair_and_push_to_gsheets():
	def fetch_from_awair():
		try:
			awair_req = requests.get(awair_url)
			sensors_dict = json.loads(awair_req.text)
			print(json.dumps(sensors_dict))
			build_gsheets_entry(sensors_dict)
		except requests.exceptions.Timeout as e:
			# timeout
			print(e)
		except requests.exceptions.ConnectionError as e:
			# connection error
			print(e)
		except requests.exceptions.RequestException as e:
			# error
			print(e)

	def build_gsheets_entry(sensors):
		for sensor in sensors.keys():
			if sensor == 'timestamp':
				sensors_list.append(str(sensors[sensor]))
			elif sensor == 'score':
				sensors_list.append(sensors[sensor])
			elif sensor == 'dew_point':
				sensors_list.append(sensors[sensor])
			elif sensor == 'temp':
				sensors_list.append(sensors[sensor])
			elif sensor == 'humid':
				sensors_list.append(sensors[sensor])
			elif sensor == 'abs_humid':
				sensors_list.append(sensors[sensor])
			elif sensor == 'co2':
				sensors_list.append(sensors[sensor])
			elif sensor == 'co2_est':
				sensors_list.append(sensors[sensor])
			elif sensor == 'voc':
				sensors_list.append(sensors[sensor])
			elif sensor == 'voc_baseline':
				sensors_list.append(sensors[sensor])
			elif sensor == 'voc_ethanol_raw':
				sensors_list.append(sensors[sensor])
			elif sensor == 'voc_h2_raw':
				sensors_list.append(sensors[sensor])
			elif sensor == 'pm25':
				sensors_list.append(sensors[sensor])
			elif sensor == 'pm10_est':
				sensors_list.append(sensors[sensor])
			elif sensor == 'lux':
				sensors_list.append(sensors[sensor])
			elif sensor == 'spl_a':
				sensors_list.append(sensors[sensor])
			else:
				print("[unknown_key] " + sensor + ": " + sensors[sensor])
		print(str(sensors_list))

	def push_to_gsheets():
		try:
			scopes = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
			credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
			service = discovery.build('sheets', 'v4', credentials=credentials)
			values = [
				sensors_list
			]
			data = {
				'values': values,
				"majorDimension": "ROWS"
			}
			service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, body=data, range=range_name, valueInputOption='USER_ENTERED').execute()
		except OSError as e:
			print(e)

	fetch_from_awair()
	push_to_gsheets()

if __name__ == '__main__':
	try:
		get_from_awair_and_push_to_gsheets()
	except KeyboardInterrupt:
		pass