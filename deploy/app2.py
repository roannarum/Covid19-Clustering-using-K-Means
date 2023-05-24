import pandas as pd
import streamlit as st

# Load the dataset
df = pd.read_csv("./dataset/covid19_dtm2.csv")
df['Fatality_Rate'] = df['Total_Deaths'] / df['Total_Cases'] * 100

# Select relevant columns and rows
df = df[['Province', 'Fatality_Rate']].dropna()

# Aggregate the data by province
df_agg = df.groupby('Province').mean().reset_index()

# Categorize the provinces based on the fatality rate
df_agg['Category'] = pd.cut(df_agg['Fatality_Rate'], bins=[-1, 1, 3, 5, float('inf')], labels=['Very Low', 'Low', 'Medium', 'High'])

# Define the app layout
st.title('COVID-19 Cases in Indonesia')

# Display a table of the provinces categorized by danger level
st.header('Provinces by Danger Level')
st.write('Tabel di bawah ini menunjukkan provinsi yang dikategorikan berdasarkan tingkat bahaya.')

# Define danger level options
options = ['Very Low', 'Low', 'Medium', 'High']

# Display selectbox to filter by danger level
st.header('Filter by Danger Level')
selected_level = st.selectbox('Pilih danger level:', options)

# Display table of provinces in selected danger level
st.write(f"Tabel di bawah ini menunjukkan provinsi yang dikategorikan sebagai '{selected_level}'")
filtered_df = df_agg[df_agg['Category'] == selected_level]
st.dataframe(filtered_df[['Province', 'Category']])
