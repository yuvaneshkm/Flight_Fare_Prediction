from flask import Flask, render_template, request
from flask_cors import cross_origin
import pickle
import sklearn
import numpy as np
from datetime import datetime
import json

app = Flask(__name__)

# Loading the model:
model=pickle.load(open("Flight_Fare_Prediction.pickle",'rb'))

# Loading Columns:
column=json.load(open("columns.json",'r'))
col=column['data_columns']



@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET","POST"])
@cross_origin()
def predict():
    if request.method=="POST":

        # No_of_stops:
        total_stops=request.form["Stops"]
        if (total_stops=='Non-stop'):
            total_stops=int(0)
        elif (total_stops=='One-stop'):
            total_stops=int(1)
        elif (total_stops=='Two-stops'):
            total_stops=int(2)

        # Depature_date:
        date=request.form["Dep_Time"]
        date_format="%Y-%m-%dT%H:%M"
        dt=datetime.strptime(date, date_format)

        jor_date=int(dt.day)
        jor_mon=int(dt.month)
        jor_day=int(dt.weekday())
        dep_hr=int(dt.hour)
        dep_min=int(dt.minute)

        # Airline:
        airline=request.form['Airline']

        # Source:
        src=request.form['Source']
        src='Source_'+src

        # Destination:
        dest=request.form['Destination']
        dest='Destination_'+dest

        a=np.zeros(len(col))

        a[0]=total_stops
        a[1]=jor_date
        a[2]=jor_mon
        a[3]=jor_day
        a[4]=dep_hr
        a[5]=dep_min

        if (airline in col):
            ind1=col.index(airline)
            a[ind1]=1
        
        if (src in col):
            ind2=col.index(src)
            a[ind2]=1

        if (dest in col):
            ind3=col.index(dest)
            a[ind3]=1

        # Prediction:
        price=model.predict([a])[0]
        fare=round(price, 2)

        return render_template('home.html', prediction_text='The Flight Fare is Rs. {}'.format(fare))
    
    return render_template('home.html')

if __name__=='__main__':
    app.run(debug=True)
    


        
