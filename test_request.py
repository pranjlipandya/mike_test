import requests

url = 'http://127.0.0.1:5000/predict'
files = {'file': open('garbage_classification/battery/battery1.jpg', 'rb')}
response = requests.post(url, files=files)

print("Status Code:", response.status_code)
if response.status_code == 200:
    print("JSON Response:", response.json())
else:
    print("Response Text:", response.text)
