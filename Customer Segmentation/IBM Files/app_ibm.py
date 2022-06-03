import numpy as np 
#import pickle 
import joblib 
import matplotlib 
import matplotlib.pyplot as plt 
import time 
import pandas 
import os 
from flask import Flask, request, jsonify, render_template

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "0yVfFM4t2gw8MpD50NnYPmVZknbBcM69ZA4_IU2yD-B9"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask (__name__) 
#model = pickle.load(open('/Users/RAHUL/Documents/Smart Bridge Externship/xgbmodel.pkl', 'rb')) 
#scale = pickle.load(open('C:/Users/SmartbridgePC/Desktop/AIML/Guided projects/rainfall_prediction/IBM flask push/Rainfall IBM deploy/scale.pkl', 'rb'))

@app.route("/")# route to display the home page 
@app.route("/home")
def home():
    return render_template('template.html') #rendering the home page 

@app.route('/predict', methods=["POST", "GET"])# route to show the predictions in a web UI 
def predict():
    # reading the inputs given by the user 
    input_feature=[float(x) for x in request.form.values() ] 
    features_values=[np.array(input_feature)] 
    names = [['Sex', 'Marital status', 'Age', 'Education', 'Income', 'Occupation','Settlement size']] 
    
    data = pandas.DataFrame(features_values, columns=names) 
    #data = scale.fit_transform(features_values)
    # predictions using the loaded model file 

    #prediction=model.predict(data) 
    #print(prediction)
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [["Sex","Marital status","Age","Education","Income","Occupation","Settlement size"]], "values": [[0,0,67,2,124670,1,2]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/e4cf614c-4242-45f8-a7bd-b200092e7e90/predictions?version=2022-05-30', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions'][0]['values'][0][0]
    print(output)
    
    if (output == 0):
       return render_template("template.html", prediction_text ="Not a potential customer")
    elif (output == 1):
       return render_template("template.html", prediction_text = "Potential customer") 
    else:
       return render_template("template.html", prediction_text = "Highly potential customer")
# showing the prediction results in a UI 

if __name__=="__main__":
# running the app
# app.run(host='0.0.0.0', port=8000, debug=True) 
    port=int(os.environ.get('PORT', 5000)) 
    app.run(port=port,debug=True,use_reloader=False)
