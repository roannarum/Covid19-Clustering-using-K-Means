import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
import streamlit as st

df = pd.read_csv('./dataset/covid_19_indonesia_time_series_all.csv')

df = df[['Province', 'Date', 'New Cases']]
df.dropna(inplace=True)

df_agg = df.groupby(['Province', 'Date']).sum().reset_index()

df_pivot = df_agg.pivot(index='Province', columns='Date', values='New Cases').fillna(0)

imputer = SimpleImputer(strategy='mean')
df_norm = imputer.fit_transform(df_pivot)

df_norm = (df_norm - df_norm.mean()) / df_norm.std()

kmeans = KMeans(n_clusters=5, random_state=42).fit(df_norm)

df_norm = pd.DataFrame(df_norm, index=df_pivot.index, columns=df_pivot.columns)
df_norm['cluster'] = kmeans.labels_

# Define the app layout
st.set_page_config(page_title='Clustering COVID-19 New Cases by Province', page_icon=':microbe:')
st.title('Clustering COVID-19 New Cases by Province')

# Add a slider to choose the number of clusters
num_clusters = st.sidebar.slider('Number of Clusters', min_value=2, max_value=10, value=5, step=1)

# Perform clustering with the chosen number of clusters
kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(df_norm)
df_norm['cluster'] = kmeans.labels_

# Display a scatter plot of the first two principal components colored by cluster
st.header('Principal Component Analysis (PCA) Plot')
st.write('The PCA plot below shows the first two principal components of the normalized data, colored by cluster.')
fig_pca = px.scatter(df_norm, x='PC1', y='PC2', color='cluster', hover_name=df_norm.index)
st.plotly_chart(fig_pca)

# Display a bar chart of the cluster sizes
st.header('Cluster Sizes')
st.write('The bar chart below shows the size of each cluster.')
fig_size = px.bar(df_norm.groupby('cluster').size().reset_index(name='count'), x='cluster', y='count')
st.plotly_chart(fig_size)
