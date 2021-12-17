from flask import Flask, render_template, request
from flask import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
import json


app = Flask(__name__, template_folder='template')
model = pickle.load(open('random_forest_regressor_model.pkl', 'rb'))



standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        input_data= (request.get_json())


        Year = int(input_data['year'])
        Present_Price = float(input_data['present_price'])
        Kms_Driven = int(input_data['kms_driven'])
        Owner = int(input_data['owner'])
        Fuel_Type = input_data['fuel_type']
        Seller_Type = input_data['seller_type']
        Transmission = input_data['transmission']


        if(Fuel_Type == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0


        elif (Fuel_Type == 'Diesel'):

            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:

            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
        Year = 2021 - Year

        if (Seller_Type == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0


        if (Transmission == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0
        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                     Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)

        if output < 0:
            #return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
            response_dict = {"price": "", "status":"Fail","response_message":"Sorry you cannot sell this car"}
            return jsonify(response_dict)
        else:
            #return render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))
            response_dict = {"price": format(output), "status": "Success",
                             "response_message": "Price prediction done"}
            return jsonify(response_dict)

    else:
        response_dict = {"price": "", "status": "Fail",
                         "response_message": "Method not allowed"}
        return jsonify(response_dict)


if __name__ == "__main__":
    app.run(debug=True)

