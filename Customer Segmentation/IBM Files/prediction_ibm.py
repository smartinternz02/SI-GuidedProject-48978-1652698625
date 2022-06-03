import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "0yVfFM4t2gw8MpD50NnYPmVZknbBcM69ZA4_IU2yD-B9"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [["Sex","Marital status","Age","Education","Income","Occupation","Settlement size"]], "values": [[0,0,67,2,124670,1,2]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e4cf614c-4242-45f8-a7bd-b200092e7e90/predictions?version=2022-05-30', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
#print(response_scoring.json())
pred=response_scoring.json()
output=pred['predictions'][0]['values'][0][0]
print(output)