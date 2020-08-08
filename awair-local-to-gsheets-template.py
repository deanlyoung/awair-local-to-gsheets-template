# -*- coding: utf-8 -*-
#!/usr/bin/env python
import json
import requests
import httplib2
import os

from datetime import datetime
from apiclient import discovery
from google.oauth2 import service_account
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

awair_url = ''

spreadsheet_id = ''
range_name = ''

# secret_file = '/path/to/client_secret.json'
secret_file = os.path.join(os.getcwd(), 'client_secret.json')


sensors_list = ["","","","","","","","","","","","","","","",""]

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
				sensor_datetime_string = sensors[sensor]
				datetime_string = datetime.strptime(sensor_datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
				sensors_list[0:1] = [datetime_string]
			elif sensor == 'score':
				sensors_list[1:2] = [sensors[sensor]]
			elif sensor == 'dew_point':
				sensors_list[2:3] = [sensors[sensor]]
			elif sensor == 'temp':
				sensors_list[3:4] = [sensors[sensor]]
			elif sensor == 'humid':
				sensors_list[4:5] = [sensors[sensor]]
			elif sensor == 'abs_humid':
				sensors_list[5:6] = [sensors[sensor]]
			elif sensor == 'co2':
				sensors_list[6:7] = [sensors[sensor]]
			elif sensor == 'co2_est':
				sensors_list[7:8] = [sensors[sensor]]
			elif sensor == 'voc':
				sensors_list[8:9] = [sensors[sensor]]
			elif sensor == 'voc_baseline':
				sensors_list[9:10] = [sensors[sensor]]
			elif sensor == 'voc_h2_raw':
				sensors_list[10:11] = [sensors[sensor]]
			elif sensor == 'voc_ethanol_raw':
				sensors_list[11:12] = [sensors[sensor]]
			elif sensor == 'pm25':
				sensors_list[12:13] = [sensors[sensor]]
			elif sensor == 'pm10_est':
				sensors_list[13:14] = [sensors[sensor]]
			elif sensor == 'lux':
				sensors_list[14:15] = [sensors[sensor]]
			elif sensor == 'spl_a':
				sensors_list[15:16] = [sensors[sensor]]
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