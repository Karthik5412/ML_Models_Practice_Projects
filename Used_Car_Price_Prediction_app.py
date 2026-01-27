import streamlit as st 
import joblib
from datetime import date
import pandas as pd

st.markdown(
    "<h1 style='text-align: center; color: #09ab3b;'>Used Car Price Prediction Model</h1>", 
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    /* Change every text element in the app to SpringGreen */
    * {
        color: #00FF7F !important;
    }
    
    /* Ensure the slider and accents follow suit */
    .stSlider > div > div > div > div {
        background-color: #00FF7F !important;
    }
    
    /* Adjust background so the green is readable */
    .stApp {
        background-color: #0E1117;
    }
    </style>
    """, unsafe_allow_html=True)

model = joblib.load('UsedCarPriceLinearRegression.plk')
scale = joblib.load('UsedCarScale.plk')
expected_cols = joblib.load('UsedCarColumns.plk')
car_models = joblib.load('UsedCarModelList.plk')
car_makers = joblib.load('UsedCarMakeList.plk')
car_variant = joblib.load('UsedCarVariantList.plk')
car_trans = joblib.load('UsedCarModelTransmissionList.plk')

# Inputs

maker = st.selectbox('Enter the brand', car_makers)

car_model = st.selectbox('Enter model of the car', car_models[maker])

variant = st.selectbox('Enter Variant',car_variant[car_model])

fuel_type = st.selectbox('Enter Fuel Type', ['petrol', 'diesel', 'petrol & cng', 'electric', 'petrol & lpg'])

transmission = st.selectbox('Enter Transmission', car_trans[variant])

yr_mfr = st.number_input('Enter Car Manufacture Year',2005,date.today().year - 2)

st.markdown("""
    <style>
    /* Change the color of the slider handle and the filled bar */
    div[data-baseweb="slider"] > div > div > div > div {
        background-color: red !important;
    }
    /* Change the color of the value label above the slider */
    div[data-testid="stThumbValue"] {
        color: red !important;
    }
    </style>
    """, unsafe_allow_html=True)
kms_run = st.slider('Enter number of km ran',10000,100000,50000)

car_rating = st.selectbox('Enter Car rating',['great', 'good', 'fair', 'overpriced', 'manual'])

st.markdown("""
    <style>
    /* Target the radio button circle when selected */
    div[data-role="radio"] div[aria-checked="true"] > div {
        background-color: skyblue !important;
        border-color: skyblue!important;
    }
    
    /* Target the outer ring of the radio button */
    div[data-role="radio"] div[aria-checked="true"] {
        border-color: skyblue !important;
    }
    </style>
    """, unsafe_allow_html=True)
is_hot = st.radio('Is this considered by many',['Yes','No'])
if is_hot == 'Yes':
    is_hot = 1
else :
    is_hot = 0
    
# Processing
if st.button('Predict'):
    input_row = {
        'yr_mfr' : [yr_mfr],
        'fuel_type_'+fuel_type : [1],
        'kms_run' : [kms_run],
        'transmission_'+transmission : [1],
        'variant_'+variant : [1],
        'is_hot' : [is_hot],
        'make_'+ maker: [1],
        'model_'+car_model : [1],
        'car_rating_'+car_rating: [1]
    }

    input_row = pd.DataFrame(input_row)
    
    for col in expected_cols:
        if col not in input_row.columns :
            input_row[col] = 0
            
    # Rows scaling 
    scale_rows = ['yr_mfr','kms_run']
    input_row[scale_rows] = scale.transform(input_row[scale_rows])
    
    final_input = input_row[expected_cols]
    
    prediction = model.predict(final_input)
    st.success(f'₹{int(prediction)}')
    
    