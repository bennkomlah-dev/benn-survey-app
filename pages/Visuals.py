# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.


try:
    df = pd.read_csv('data.csv')
    st.success("CSV data loaded successfully!")
except:
    st.error("Could not load data.csv")
    df = pd.DataFrame()
with open('data.json') as infile:
    json_data = json.load(infile)


# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Average Daily Screen Time by Device")# CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("This static graph shows the average hours per day spent on each device based on survey responses.")
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
if not df.empty:
    avg_df = df.groupby('Device')['Hours'].mean().reset_index()
    st.bar_chart(data=avg_df, x='Device', y='Hours', color="#CC5500")

st.divider()
# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Explore Survey Results") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("Select a device and set a maximum hour limit to filter and update the graph.")
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.
if "selected_device" not in st.session_state:
    st.session_state["selected_device"] = "All"
if "max_hours" not in st.session_state:
    st.session_state["max_hours"] = 24
if not df.empty:
    all_devices = ["All"] + df['Device'].unique().tolist()
    selected_device = st.selectbox("Select a device:", all_devices)
    st.session_state["selected_device"] = selected_device
    max_hours = st.slider("Max hours per day:", 1, 24, 24)
    st.session_state["max_hours"] = max_hours
    if st.session_state["selected_device"] == "All":
        filtered_df = df[df['Hours'] <= st.session_state["max_hours"]]
    else:
        filtered_df = df[
            (df['Device'] == st.session_state["selected_device"]) &
            (df['Hours'] <= st.session_state["max_hours"])
        ]
    if not filtered_df.empty:
        st.line_chart(data=filtered_df, x='Device', y='Hours', color="#0000FF")
    else:
        st.warning("No data matches your filters.")

st.divider()
# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Screen Time by App Category") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("Select a category and sort order to explore average screen time per app category.")
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "All"
if "sort_order" not in st.session_state:
    st.session_state["sort_order"] = "Original"
json_df = pd.DataFrame(json_data['data_points'])
json_df.columns = ['Category', 'Hours']
all_categories = ["All"] + json_df['Category'].tolist()
selected_category = st.selectbox("Select an app category:", all_categories)
st.session_state["selected_category"] = selected_category
sort_order = st.radio("Sort by hours:", ["Original", "Ascending", "Descending"])
st.session_state["sort_order"] = sort_order
if st.session_state["selected_category"] == "All":
    filtered_json = json_df.copy()
else:
    filtered_json = json_df[json_df['Category'] == st.session_state["selected_category"]]
if st.session_state["sort_order"] == "Ascending":
    filtered_json = filtered_json.sort_values('Hours', ascending=True)
elif st.session_state["sort_order"] == "Descending":
    filtered_json = filtered_json.sort_values('Hours', ascending=False)
if not filtered_json.empty:
    st.bar_chart(data=filtered_json, x='Category', y='Hours', color="#00AA00")
else:
    st.warning("No data to display.")
