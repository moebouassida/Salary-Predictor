import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



#leaving all countries with high count value
def clean_country(ctr, count):
    #store all countries
    ctr_dict = {}
    for i in range(len(ctr)):
        if ctr.values[i] >= count:
            ctr_dict[ctr.index[i]] = ctr.index[i]
        else:
            ctr_dict[ctr.index[i]] = 'Others'
    return ctr_dict

def clean_education(x):
    if x == 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)':
        return 'Bachelor’s degree'
    if x == 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)':
        return 'Master’s degree'
    if x == 'Professional degree (JD, MD, Ph.D, Ed.D, etc.)':
        return 'Professional degree'
    return 'Lower than Bachelor’s degree'

def clean_exp(x):
    if x == 'Less than 1 year':
        return 0.5
    if x == 'More than 50 years':
        return 50
    return float(x)

@st.cache_data
def load_data():
    
    df = pd.read_csv("survey_results_public.csv")
    df = df.loc[:, ['EdLevel', 'Country', 'ConvertedCompYearly', 'YearsCodePro']]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    df = df.rename({'YearsCodePro':'Experience'}, axis=1)
    df = df.dropna()
    
    ctr_dict = clean_country(df.Country.value_counts(), 350)
    df.Country = df.Country.map(ctr_dict)

    df = df[df.Salary <= 300000]
    df = df[df.Salary >= 20000]
    df = df[df.Country != 'Others']

    df.EdLevel = df.EdLevel.apply(clean_education)
    df.Experience = df.Experience.apply(clean_exp)
    
    return df

df = load_data()

def show_explore_page():
    st.title("Software Developer Salary Prediction")
    
    st.write("""### Stack Overflow Developer Survey 2023""")

    data = df.Country.value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index)
    ax1.axis("equal")

    st.write("""### Data From Different Countries""")
    
    st.pyplot(fig1)

    st.write("""### Mean Salary Based On Country""")

    data = df.groupby(['Experience'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Mean Salary Based On Experience""")

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)