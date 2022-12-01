import joblib
import streamlit as st
import numpy as np

model = joblib.load('model_publicite.joblib')['model']
scaler = joblib.load('model_publicite.joblib')['scaler']

def commande(model, age, salary):
    """Retourne si oui ou non un individu est susceptible d'acheter un produit"""
    achat = {0:"pas d'achat", 1:"achat"}
    x = np.array([age, salary]).reshape(1,2)
    x_scaled = scaler.transform(x)
    return achat[model.predict(x_scaled)[0]]

st.title("App Marketing Ads")
age = st.slider('Age',18,60,50)
salary = st.slider('Salaire annuel', 15000,150000,40000)

prediction = commande(model, age, salary)
st.write(prediction)
