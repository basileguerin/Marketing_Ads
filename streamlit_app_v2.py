import joblib
import streamlit as st
import numpy as np
import pandas as pd
import mysql.connector as mysqlpy

bdd = mysqlpy.connect(user='root', password='example', host='localhost', port='3307', database='Marketing_Ads')
cursor = bdd.cursor()

model = joblib.load('model_publicite.joblib')['model']
scaler = joblib.load('model_publicite.joblib')['scaler']

def get_data():
    """Recupère les id, ages et salaires des users et les stocke
    dans des listes"""
    query = """SELECT userID, age, salary FROM users"""
    cursor.execute(query)
    for i in cursor:
        ids.append(i[0])
        ages.append(i[1])
        salaries.append(i[2])

def commande(model, age, salary):
    """Retourne si oui ou non un individu est susceptible d'acheter un produit"""
    achat = {0:"pas d'achat", 1:"achat"}
    x = np.array([age, salary]).reshape(1,2)
    x_scaled = scaler.transform(x)
    return achat[model.predict(x_scaled)[0]]

def add_buyers():
    """Rempli la table acheteurs avec les id des users qui vont
    potientiellement acheter"""
    for i in range(len(ages)):
        age = ages[i]
        salary = salaries[i]
        id = ids[i]
        predict = commande(model, age, salary)
        if predict =='achat':
            query = f"""INSERT INTO acheteurs(id_acheteur) VALUES ({id})
            ON DUPLICATE KEY UPDATE id_acheteur={id}"""
            cursor.execute(query)

st.title('App Marketing V2')

with st.form('add_user', clear_on_submit=True):
    st.subheader('add_user')
    gender = st.radio("gender :", ('Male', 'Female'))
    age = st.slider("age :", 0, 100)
    salary = st.slider("annual salary :", 0, 150000)
    submitted = st.form_submit_button('Submit')
    if submitted:
        query = f"""INSERT INTO users(gender, age, salary) VALUES ('{gender}', {age}, {salary});"""
        cursor.execute(query)

if st.button('get_users'):
    query = """SELECT * FROM users"""
    cursor.execute(query)
    users = []
    for i in cursor:
        users.append(i)
    df = pd.DataFrame(data=users, columns=['id', 'gender', 'age', 'annual salary'])
    st.write(df)

if st.button('get_buyers'):
    ids = []
    ages = []
    salaries = []
    get_data()
    add_buyers()
    query = """SELECT * FROM acheteurs"""
    cursor.execute(query)
    buyers = []
    for i in cursor:
        buyers.append(i)
    df = pd.DataFrame(data=buyers, columns=['id_user'])
    st.write(df)

bdd.commit()
cursor.close()
bdd.close()
