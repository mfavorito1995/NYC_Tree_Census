import streamlit as st
import pandas as pd
import plotly.express as px
import glob

st.set_page_config(
    page_title="Street Tree Species",
    page_icon=':deciduous_tree:',
    layout="wide"
)

@st.cache
def load_trees_data():
    data = pd.concat(map(pd.read_csv, glob.glob(r"data\trees_boro_data\*")), ignore_index=True)

    # data = pd.read_csv(r'C:\Users\Mark\NYC Tree Data\2015StreetTreesCensus_TREES.csv', usecols=usecols)
    data.rename({'Latitude': 'latitude'}, inplace=True)
    data['spc_common'] = data['spc_common'].str.title()
    return data


def species_map(data):
    fig = px.scatter_mapbox(data, lat="Latitude", lon="longitude", hover_data=["address"],
                            color_discrete_sequence=["green"], zoom=9,
                            center={"lat": 40.71264206172198648, "lon": -73.95069249193706},
                            height=700)
    fig.update_layout(mapbox_style="carto-positron")

    return fig


@st.cache
def load_trees_species_count():
    species_count = pd.read_csv('data/common_species_count.csv')
    return species_count


def top_20_species_chart(species_count):
    fig = px.bar(species_count.nlargest(n=20, columns=['count']), x='spc_common', y='count', color='count',
                 labels={"spc_common": "Species",
                         "count": "Count"},
                 color_continuous_scale='algae', range_color=[0, 100000])
    return fig


def bottom_20_species_chart(species_count):
    fig = px.bar(species_count.nsmallest(n=20, columns=['count']), x='spc_common', y='count', color='count',
                 labels={"spc_common": "Species",
                         "count": "Count"},
                 color_continuous_scale='algae', range_color=[0, 100])

    return fig


# Load or reload trees data if needed
data = load_trees_data()
if 'data' not in st.session_state:
    data = load_trees_data()
    st.session_state.data = data

species = load_trees_species_count()
top20chart = top_20_species_chart(species)
bottom20chart = bottom_20_species_chart(species)

st.title('A Look at the NYC Tree Census of 2015')

# Notify the reader that the data was successfully loaded.
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
data_load_state.text('Loading data...done!')

st.header('Street Tree Species')

st.markdown("### Most and Least Common Trees")

st.markdown("Now, let's take a look at all the different species of trees found on New York's streets. "
            "These two charts show the 20 most and least common trees in the city, while the interactive table to the right lists out the count for every identified species.")

coll, col1, col2, colgap, coltable, colr = st.columns([0.2, 2, 2, 0.25, 1, 0.2])

col1.subheader("20 Most Common Species")
col1.plotly_chart(top20chart, use_container_width=True)

col2.subheader("20 Least Common Species")
col2.plotly_chart(bottom20chart, use_container_width=True)

coltable.subheader('All Species')
coltable.dataframe(species)

st.markdown('### Interactive Species Map')

st.markdown("Finally, let's explore where we can find each species. "
            "Select a species from the drop down, and then check out the map below to see where we can find it. "
            "The trees are sorted alphabetically, so be sure to look for the most and least common species!")

col3, colmap, col4 = st.columns([1, 3, 1])

with colmap:
    option = st.selectbox(
        'Select a species',
        (list(species['spc_common'].unique())))

    species_to_filter = option
    filtered_data = data[data['spc_common'] == species_to_filter]
    st.subheader(f'Map of {species_to_filter}')
    species_map = species_map(filtered_data)
    st.plotly_chart(species_map, use_container_width=True)

st.markdown("Thanks for reading! Send any questions or thoughts to mfavorito1995@gmail.com.")

st.markdown(
    "Curious to learn more? You can read more about this great project at this link: https://www.nycgovparks.org/trees/treescount.")
