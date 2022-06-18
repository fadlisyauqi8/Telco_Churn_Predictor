import streamlit as st
import requests
import json
from PIL import Image

st.set_page_config(layout="centered", page_icon="✈️", page_title="Telco Customer Churn Predictor")
st.title("Telco Customer Churn Predictor")
st.subheader('This apps will help predict customer who will churn or not')

image = Image.open('HeaderFront.png')
st.image(image, use_column_width = True, caption='Telco Churn Predictor')

st.header("Customer Telco Information")
st.write("Please input customer information")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Select Gender Customer", ['Male', 'Female'])
    Partner = st.selectbox("Select If Customer Has Partner", ['No', 'Yes'])
with col2:
    Dependents = st.selectbox("Select If Customer Still Dependents", ['No', 'Yes'])
    SeniorCitizen = st.selectbox("Select If Customer Senior Citizen (0 = No, 1 = Yes)", ['0', '1'])

st.header("Customer Payment Information")
st.write('Input your payment information')

col1, col2 = st.columns(2)
with col1:
    tenure = st.number_input("Input The Tenure of Customer", value=0, min_value=0, max_value=100)
    MonthlyCharges = st.number_input("Input The Monthly Charges of Customer", value=0, min_value=0, max_value=150)
with col2:
    Contract = st.selectbox("Select The Contract Type", ['Month-to-month', 'One year', 'Two year'])
    PaperlessBilling = st.selectbox("Select If Customer Use Paperless Billing", ['No', 'Yes'])

PaymentMethod = st.selectbox("Select The Payment Method", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])

st.header("Customer Service Information")
st.write('Please choose what service you subscribed')

MultipleLines = st.selectbox("Select If Customer Have Multiple Lines", ['No', 'Yes', 'No phone service'])
InternetService = st.selectbox("Select If Cusomer Has The Internet Service", ['DSL', 'Fiber optic', 'No'])
if InternetService == 'No':
    StreamingMovies = st.selectbox("Select If Customer Subscribe Streaming Movies", ['No internet service'])
    OnlineSecurity = st.selectbox("Select If Customer Has Online Security", ['No internet service'])
    OnlineBackup = st.selectbox("Select If Customer Has Online Backup", ['No internet service'])
    DeviceProtection = st.selectbox("Select If Customer Has Device Protection", ['No internet service'])
    TechSupport = st.selectbox("Select If Customer Has Tech Support", ['No internet service'])

else:
    StreamingMovies = st.selectbox("Select If Customer Subscribe Streaming Movies", ['No', 'Yes'])
    OnlineSecurity = st.selectbox("Select If Customer Has Online Security", ['No', 'Yes'])
    OnlineBackup = st.selectbox("Select If Customer Has Online Backup", ['No', 'Yes'])
    DeviceProtection = st.selectbox("Select If Customer Has Device Protection", ['No', 'Yes'])
    TechSupport = st.selectbox("Select If Customer Has Tech Support", ['No', 'Yes'])




# Inference Set
data = {'tenure' : tenure,
        'MonthlyCharges' : MonthlyCharges,
        'gender' : gender,
        'SeniorCitizen' : SeniorCitizen,
        'Partner' : Partner,
        'Dependents' : Dependents,
        'MultipleLines' : MultipleLines,
        'InternetService' : InternetService,
        'OnlineSecurity' : OnlineSecurity,
        'OnlineBackup' : OnlineBackup,
        'DeviceProtection' : DeviceProtection,
        'TechSupport' : TechSupport,
        'StreamingMovies' : StreamingMovies,
        'Contract' : Contract,
        'PaperlessBilling' : PaperlessBilling,
        'PaymentMethod' : PaymentMethod}

URL = "https://churn-backend.herokuapp.com/predict"    


#komunikasi

churn_prediction = st.button('Predict')
if churn_prediction :
    r = requests.post(URL, json=data)
    res = r.json()
    
    if res['code'] == 200:
        res2 = (res['result'])
        if res2 == 'No':
            st.markdown(''' <h2> Customer Stay </h2>''', unsafe_allow_html=True)
            col4,col5,col6 = st.columns([1,1,1])
            with col5 : 
                st.image('NoResult.png')
                st.balloons()
        else:
            st.markdown(''' <h2> Customer Leaving </h2>''', unsafe_allow_html=True)
            col7,col8,col9 = st.columns([1,1,1])
            with col8:
                st.image('YesResult.png')
                st.snow()
    else:
        st.write("Error....")
        st.write(f"Details : {res['result']['error_msg']}")