import requests

r = requests.get('http://localhost:7071/api/big_trig')

print(r.text)
print(r.status_code)

