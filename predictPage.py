import streamlit as st
import pickle 
import numpy as np


def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

reg = model['model']
ctr_encoder = model['ctr_enc']
edu_encoder = model['edu_enc']


def show_predict_page():
    countries = [   
    "United States of America",                                                                              
    "Germany",                                                 
    "United Kingdom of Great Britain and Northern Ireland",     
    "Canada",                                                   
    "India",                                                  
    "France",                                                   
    "Netherlands",                                              
    "Poland",                                                   
    "Brazil",                                                   
    "Australia",                                                
    "Spain",                                                    
    "Sweden",                                                   
    "Italy",                                                    
    "Switzerland",                                               
    "Austria",                                                   
    "Denmark",                                                   
    "Czech Republic",                                        
    "Norway",                                                    
    "Portugal",                                                  
    "Israel",                                                    
    "Belgium",                                                   
    "Finland",                                                   
    "Russian Federation",                                        
    "Ukraine",                                                   
    "New Zealand",                                               
    "Romania",                                                   
    "Turkey",                                                    
    "South Africa",  
            ]

    education = [
        "Lesser than Bachelor’s degree",
        "Bachelor's degree",
        "Master's degree",
        "Post grad"
                ]

    st.title("Software Developer Salary Prediction")
    
    st.write("""### We need some information to predict the salary""")
    
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    experience = st.slider("Years of Experience", 0, 50, 1)

    button = st.button("Predict Salary")
    if button: 
        X = np.array([[education, country, experience]])
        X[:, 0] = edu_encoder.transform(X[:,0])
        X[:, 1] = ctr_encoder.transform(X[:,1])
        X = X.astype(float)

        salary = reg.predict(X)
        st.subheader(f"The estimated salary is {salary[0]:.2f} $")





