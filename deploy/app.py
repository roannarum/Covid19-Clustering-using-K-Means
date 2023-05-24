import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import tornado.web
import seaborn as sns
import plotly.express as px
from plotly import graph_objs as go

st.set_page_config(page_title="Covid-19 Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# --- Load Data From CSV ----
@st.cache_data
def get_data_from_csv():
    df = pd.read_csv("./dataset/covid19_dtm2.csv")
    df_all = pd.read_csv("./dataset/covid_19_indonesia_time_series_all.csv")
    return df,df_all
df,df_all = get_data_from_csv()

# --- Header ---
st.header(":bar_chart: Indonesia Covid-19")
st.markdown("----")

# --- Informasi total data ---
total_case, total_recovered, total_death = st.columns(3)

total_case.metric("Total Kasus", df.New_Cases.sum())
total_recovered.metric("Total Sembuh",  df.New_Recovered.sum())
total_death.metric("Total Meninggal",  df.New_Deaths.sum())\

st.markdown("----")

# Tampilkan daftar provinsi
provinces = df['Province'].unique().tolist()
province_filter = st.sidebar.multiselect('Filter berdasarkan provinsi:', provinces)

# Filter data berdasarkan provinsi yang dipilih
if province_filter:
    df = df[df['Province'].isin(province_filter)]

# Tampilkan data yang sudah difilter
st.write(df)

st.markdown("---")
# --- sidebar ---
st.sidebar.write('Pilih Jenis Data:')
option_1 = st.sidebar.checkbox('Total Kasus')
option_2 = st.sidebar.checkbox('Kasus Harian')
option_3 = st.sidebar.checkbox('Total Sembuh')
option_4 = st.sidebar.checkbox('Sembuh Harian')
option_5 = st.sidebar.checkbox('Total Meninggal')
option_6 = st.sidebar.checkbox('Meninggal Harian')

fig_main = go.Figure()
if (option_1 or option_2 or option_3 or option_4 or option_4 or option_5 or option_6) is False:
    fig_main.add_trace(go.Scattergl(x=df['Date'], y=df['New_Cases'], name='Kasus Harian'))
    fig_main.add_trace(go.Scattergl(x=df['Date'], y=df['New_Recovered'], name='Sembuh Harian'))
else:
    if option_1:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['Total_Newcases'], name='Total Kasus'))
    if option_2:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['New_Cases'], name='Kasus Harian'))
    if option_3:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['Total_Recovered'], name='Total Sembuh'))
    if option_4:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['New_Recovered'], name='Sembuh Harian'))
    if option_5:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['Total_Deaths'], name='Total Meninggal'))
    if option_6:
        fig_main.add_trace(go.Scatter(x=df['Date'], y=df['New_Deaths'], name='Meninggal Harian'))
fig_main.layout.update(title_text='Indonesia Covid-19', 
                       xaxis_rangeslider_visible=True, 
                       hovermode='x',
                       legend_orientation='v')

st.plotly_chart(fig_main, use_container_width=True)

st.markdown("---")

provinsi_p = df.groupby('Province')['Total_Newcases'].sum().reset_index()

n_prov = st.slider('jumlah Provinsi:', 1, len(provinsi_p), 4)

top_prov = provinsi_p.nlargest(n_prov, 'Total_Newcases')

st.bar_chart(top_prov.set_index('Province'))

st.markdown("---")

# input untuk correlation matrix
import pandas as pd
import streamlit as st

df['Case_Fatality_Rate'] = df['Total_Deaths'] / df['Total_Cases'] * 100

if st.checkbox("Tampilkan korelasi matriks"):
    selected_cols = st.multiselect("Pilih kolom yang ingin dianalisis", df.columns.tolist() + ['Case_Fatality_Rate'])
    corr_method = st.selectbox("Metode korelasi", ("pearson", "kendall", "spearman"))

    if len(selected_cols) > 0:
        corr_data = df[selected_cols].corr(method=corr_method)
        st.write("Korelasi Matriks:")
        st.write(corr_data)
    else:
        st.warning("Silahkan pilih minimal 1 kolom untuk dianalisis.")

st.markdown("---")


# Compute the fatality rate
df['Fatality_Rate'] = df['Total_Deaths'] / df['Total_Cases'] * 100

# pilih relevant columns dan rows
df = df[['Province', 'Fatality_Rate']].dropna()

# Aggregate data by province
df_agg = df.groupby('Province').mean().reset_index()

#mengkategorikan fatality menjadi 3
df_agg['Category'] = pd.cut(df_agg['Fatality_Rate'], bins=[1, 2, 3, float('inf')], labels=['Low', 'Medium', 'High'])

#judul tampilan terakhir
st.title('COVID-19 Cases in Indonesia')

st.header('Provinces by Danger Level')
st.write('Tabel di bawah ini menunjukkan provinsi yang dikategorikan berdasarkan tingkat bahaya.')

# opsi level options
options = ['Low', 'Medium', 'High']

# Display selectbox to filter by danger level
st.header('Filter by Danger Level')
selected_level = st.selectbox('Pilih danger level:', options)

#menampilkan rekomendasi jika telah memilih
if selected_level == 'Low':
    st.write("Direkomendasikan untuk PPKM LEVEL 1 - 2")
elif selected_level == 'Medium':
    st.write("Direkomendasikan untuk PPKM LEVEL 3, serta direkomendasikan untuk melakukan vaksinasi")
else:
    st.write("Direkomendasikan untuk PPKM LEVEL 4, serta direkomendasikan untuk melakukan vaksinasi dan penambahan fasilitas kesehatan")

# tampilkan tabel
st.write(f"Tabel di bawah ini menunjukkan provinsi yang dikategorikan sebagai '{selected_level}'")
filtered_df = df_agg[df_agg['Category'] == selected_level]
st.dataframe(filtered_df[['Province', 'Category']])

