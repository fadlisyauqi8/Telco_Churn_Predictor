from flask import Flask, jsonify, request
import pickle
import pandas as pd
import numpy as np
from tensorflow import keras



app = Flask(__name__)

# Open Pickle Save
with open("pipe_Pre.pkl", "rb") as f:
    pipe_Pre = pickle.load(f)

# Open Model
model = keras.models.load_model('model.h5')

results = ['No', 'Yes']
columns = ['tenure','MonthlyCharges', 'gender', 'SeniorCitizen', 'Partner',
 'Dependents', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 
 'DeviceProtection', 'TechSupport', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']

@app.route("/")
def home():
    return "<h1>Welcome!</h1>"


@app.route("/predict", methods=['GET','POST'])
def model_prediction():
    if request.method == "POST":
        content = request.json
        try: 
            data= [content['tenure'],
                   content['MonthlyCharges'],
                   content['gender'],
                   content['SeniorCitizen'],
                   content['Partner'],
                   content['Dependents'],
                   content['MultipleLines'],
                   content['InternetService'],
                   content['OnlineSecurity'],
                   content['OnlineBackup'],
                   content['DeviceProtection'],
                   content['TechSupport'],
                   content['StreamingMovies'],
                   content['Contract'],
                   content['PaperlessBilling'],
                   content['PaymentMethod']]
            data = pd.DataFrame([data], columns = columns)
            data = pipe_Pre.transform(data)
            res = model.predict(data)
            print(res) # Check proba from response
            res = np.where(res < 0.25, 0, 1) #Change Threshold from 0.5 to 0.25
            print('res : ', res, type(res)) # Check type response


            response = {'code' : 200, 'status' : 'OK', 'result' : results[int(res[0][0])]} # numpy 2d array
            print(response)
            return jsonify(response)

        except Exception as e :
                    response2 = {'code' : 400, 'status' : 'Error', 'result' : {'error_msg' : str(e)}}
                    return jsonify(response2)

    return "<p> Please Use Post Methods To Access The Prediction </p>"

#app.run(debug=True)
