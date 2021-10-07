import requests

x = requests.get('https://w3schools.com')
print(x.status_code)

# set FLASK_APP=pythonapp
# set FLASK_ENV=development
