import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import pandas as pd
import plotly.express as px
import numpy as np
from newsapi import NewsApiClient
import requests


st.title("Keep Philly Safe and Aware")

st.sidebar.header("Map Type")
options = ['Crimes', 'Safety Rating']
selected_option = st.sidebar.selectbox("What map would you like to see", options)

def plot_points_on_map(filename, selected_option):
    data = pd.read_csv(filename)

    m = folium.Map(location=[data.iloc[0]['Latitude'], data.iloc[0]['Longitude']], zoom_start=11)

    for index, row in data.iterrows():
        if selected_option == 'Crimes':
            icon_color = 'red'
        elif selected_option == 'Safety Rating':
            score = row[1]
            if score > 70:
                icon_color = 'green'
            elif 50 <= score <= 70:
                icon_color = 'yellow'
            else:
                icon_color = 'red'

        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row[1],  
            icon=folium.Icon(color=icon_color)
        ).add_to(m)

    map_filename = "map.html"
    m.save(map_filename)
    return map_filename

if selected_option == 'Crimes':
    csv_file_path = 'crimestat.csv'
    icon_color = 'red'
elif selected_option == 'Safety Rating':
    csv_file_path = 'safetyrating.csv'
    icon_color = None  


map_filename = plot_points_on_map(csv_file_path, selected_option)


st.subheader("Crime Map" if selected_option == 'Crimes' else "Safety Rating Map")
st.components.v1.html(open(map_filename).read(), width=700, height=500)

news,stats = st.tabs(["News Stories", "Statistics" ])

with news:
    st.header("News for Philly")
    NEWS_API_KEY = "9af5fb82daac40c09eb729a4f7779214"  
    NEWS_API_URL = "https://newsapi.org/v2/everything"

    def fetch_philadelphia_headlines():
        params = {
            "apiKey": NEWS_API_KEY,
            "q": "Philadelphia",
            "pageSize": 10  
        }

        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("articles", [])
        else:
            st.error("Failed to fetch Philadelphia headlines.")
            return []


    headlines = fetch_philadelphia_headlines()
    if headlines:
        for article in headlines:
            st.write(f"**{article['title']}**")
            st.write(f"Source: {article['source']['name']}")
            st.write(f"Description: {article['description']}")
            st.write(f"URL: {article['url']}")
            st.write("---")

            
with stats:
    
    st.header("Philadelphia Annual Crime Stats")
    data = {
    '': [ "Number of Crimes", "Crime Rate (Per 1,000 Residents)"],
    'Violent': [ '12,788', '8.11'],
    'Property': [ '41,847', "26.55"],
    'Total': ['54,635', '34.66']
    }

    df = pd.DataFrame(data)
    st.table(df)
    st.write("According to Neighborhood Scout")


    st.header("2023 Gun Violence Incidents By Neighborhood")
    def load_data():
        data = pd.read_csv('hackathon_data.csv')
        return data

    data = load_data()
    fig = px.bar(data, x= 'count', y = 'Neighborhood')
    st.plotly_chart(fig)
    st.write('According to the Office of the Controller')


