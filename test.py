import requests as r

# This is the base URL, change this based on what is printed by the flask application
BASE = "http://127.0.0.1:5000/"

# This is an example of using a get request from the server
# Possible types are GET, POST, PUT, PATCH or HEAD
# Preface each request to a route with the base URL provided above
response = r.get(BASE)

# Print the reponse in the JSON format
print(response.json())