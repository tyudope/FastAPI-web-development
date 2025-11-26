import requests


r = requests.get("http://localhost:8000/hi")
# r = requests.get("http://localhost:8000/hi/stefan") -> URL PATH Test
# r = requests.get("http://localhost:8000/hi&who=Mom") -> Query Parameter Test.

# Requests with params.
params = {"who" : "mom"}
r = requests.get("http://localhost:8000/hi", params = params)


# Test with requests, which uses its JSON arguments to pass JSON-Encoded data in the request body
r = requests.post("http://localhost:8000/hi", json = {"who":"knight"})




print(r.json())
