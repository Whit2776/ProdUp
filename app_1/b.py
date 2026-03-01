from plyer import notification
import time
import requests
import pyautogui
api_url = 'https://jsonplaceholder.typicode.com/posts/1'

try:
  response = requests.get(api_url)
  if response.status_code == 200:
    data = response.json()
    print('Fetched Data: \n', data)
  else:
    print('You have an error', response.status_code)
except requests.exceptions.RequestException as e:
  print('You have an error: \n', e)

while input():
  notification.notify(
    title = 'ALERT',
    message = 'Take a break man, it"s been an hour',
    timeout = 10
  )

  time.sleep(3600)