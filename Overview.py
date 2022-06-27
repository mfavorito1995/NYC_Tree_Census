import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_folium
import geopandas as gpd
import json
import glob


st.set_page_config(
    page_title="NYC Tree Census",
    page_icon=':deciduous_tree:',
    layout="wide"
)

st.title('A Look at the NYC Tree Census of 2015')

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.markdown('### Introduction')

st.markdown("In 2015 the city of New York conducted its third Street Tree Census. "
            "City employees and volunteers *(also known as voluntreers)* went block by block to count all of the leafy friends lining the streets of the five boros. "
            "According to the Parks Department's website, this effort brought together **more than 2,200 volunteers** who counted a total of **666,134 trees** using a combination of old school tools and high tech interactive maps. "
            "Importantly, as its name makes clear, this census only counted trees lining the streets and *not* those found in the city's many parks.")

st.markdown(
    "While a tree census may sound like just a fun bureaucratic exercise, understanding the landscape of city streets can have a real impact on New Yorkers' daily lives. "
    "Street trees benefit residents in many ways such as improving air quality, reducing stormwater runoff, and lessening the urban heat island effect - all in addition to making streets more beautiful. "
    "All told, the city has estimated that in addition to looking beautiful, street trees have created $151.2 million in benefits to New York City. ")

st.markdown(
    "Understanding these benefits, the city aims to use the data collected in their tree census to help them make better public policy decisions. "
    "Since conducting the first Street Tree Census in 1995, the city has been better equipped to direct funding for greening intiatives, ultimately improving the lives of all New Yorkers.")

st.markdown("Now, as a geospatial nerd, this census provided me with tons of fun new data to play with. "
            "I've created this page to help do just that. **Scroll on to learn more!**")


def boroughs_map():
    boroughs_gpd = gpd.read_file(r'data\boroughs_with_stats.geojson').set_index("Boro")

    m = px.choropleth_mapbox(boroughs_gpd, geojson=boroughs_gpd.geometry, locations=boroughs_gpd.index,
                             color=boroughs_gpd['Count of Trees'],
                             color_continuous_scale="YlGn",
                             mapbox_style="carto-positron",
                             zoom=9, center={"lat": 40.71264206172198648, "lon": -73.95069249193706},
                             opacity=0.5,
                             labels={'Count of Trees': 'Count of Trees'},
                             height=700
                             )
    return m


def nta_map():
    nta_gpd = gpd.read_file(r'data\ntas_with_stats.geojson').set_index("NTA")

    m = px.choropleth_mapbox(nta_gpd, geojson=nta_gpd.geometry,
                             locations=nta_gpd.index,
                             color=nta_gpd['Count of Trees'],
                             color_continuous_scale="YlGn",
                             mapbox_style="carto-positron",
                             zoom=9, center={"lat": 40.71264206172198648, "lon": -73.95069249193706},
                             opacity=0.5,
                             labels={'NTA': 'NTA', 'Count of Trees': 'Count of Trees'},
                             height=700
                             )

    return m


def hex_map():
    hex_gpd = gpd.read_file(r'data\quarter_mile_trees.geojson')

    m = px.choropleth_mapbox(hex_gpd, geojson=hex_gpd.geometry,
                             locations=hex_gpd.index,
                             color=hex_gpd['Count Trees'],
                             color_continuous_scale="YlGn",
                             mapbox_style="carto-positron",
                             zoom=9, center={"lat": 40.71264206172198648, "lon": -73.95069249193706},
                             opacity=0.5,
                             labels={'Count of Trees': 'Count Trees'},
                             height=700
                             )
    m.update_traces(marker_line_width=0)

    return m


def boro_counts(species_boro_count):
    bronx = species_boro_count.loc[species_boro_count['Boro'] == 'Bronx'].sort_values(by='Count', ascending=False)
    brooklyn = species_boro_count.loc[species_boro_count['Boro'] == 'Brooklyn'].sort_values(by='Count', ascending=False)
    manhattan = species_boro_count.loc[species_boro_count['Boro'] == 'Manhattan'].sort_values(by='Count',
                                                                                              ascending=False)
    queens = species_boro_count.loc[species_boro_count['Boro'] == 'Queens'].sort_values(by='Count', ascending=False)
    staten_island = species_boro_count.loc[species_boro_count['Boro'] == 'Staten Island'].sort_values(by='Count',
                                                                                                      ascending=False)

    boro_counts = {'The Bronx': bronx, 'Brooklyn': brooklyn,
                   'Manhattan': manhattan, 'Queens': queens,
                   'Staten Island': staten_island}
    return boro_counts

boroughs_map = boroughs_map()
nta_map = nta_map()
hex_map = hex_map()

st.markdown('### Street Tree Overview')

st.markdown("First, let's orient ourselves and take a look at where these 600,000+ street trees are. "
            "To do this, I've created three maps showing the distribution of street trees across the city. "
            "The first map breaks down the count of trees by Boro, the second does the same by Neighborhood Tabulation Area, and the third shows trees aggregated up into 1/4 square mile hex-grids. "
            "Looking at the trees in these three ways, starting very generally, and ending more granularly, we can get a real sense of the city's landscape. ")

st.markdown("Click through the maps and pan around to explore the leafy landscape:")

bl, omap, br = st.columns([1, 3, 1])
with omap:

    map_option = st.radio(
        'Select a geography',
        (['Boro', 'Neighborhood Tabulation Area', '1/4 Sq Mile Hex-Grid']),
        horizontal=True)

    map_to_make = map_option
    st.subheader(f'Trees by {map_option}')

    if map_option == 'Boro':
        st.plotly_chart(boroughs_map, use_container_width=True)
    elif map_option == 'Neighborhood Tabulation Area':
        st.plotly_chart(nta_map, use_container_width=True)
    elif map_option == '1/4 Sq Mile Hex-Grid':
        st.plotly_chart(hex_map, use_container_width=True)

st.markdown(
    "##### Click the Species tab to read on and explore the types of trees found on NYC streets!")

st.markdown(
    "Curious to learn more? You can read more about this great project at this link: https://www.nycgovparks.org/trees/treescount.")
