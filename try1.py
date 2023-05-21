import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import requests
import matplotlib.pyplot as plt

import streamlit as st

import streamlit as st
import pandas as pd

def load_data(file):
    if file is not None:
        if file.type == 'application/vnd.ms-excel':
            df = pd.read_excel(file, engine='openpyxl')
        elif file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df = pd.read_excel(file)
        elif file.type == 'text/csv':
            df = pd.read_csv(file)
        else:
            df = None
        return df

def upload_file():
    st.set_option('deprecation.showfileUploaderEncoding', False)
    uploaded_file = st.file_uploader("Upload your file here", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.write("Data loaded successfully:")
            st.write(df.head())
            return df
        else:
            st.write("Failed to load data.")
    else:
        st.write("No file uploaded.")





def display_line_chart(df, x_col, y_col):
    # Create a line chart
    fig, ax = plt.subplots()
    ax.plot(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title("Line Chart")

    # Display the chart in Streamlit
    st.pyplot(fig)

def display_bar_chart(df, x_col, y_col):
    # Create a bar chart
    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title("Bar Chart")

    # Display the chart in Streamlit
    st.pyplot(fig)

def display_pie_chart(df, x_col, y_col):
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(df[y_col], labels=df[x_col], autopct='%1.1f%%')
    ax.set_title("Pie Chart")

    # Display the chart in Streamlit
    st.pyplot(fig)

def display_area_chart(df, x_col, y_col):
    # Create an area chart
    fig, ax = plt.subplots()
    ax.fill_between(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title("Area Chart")

    # Display the chart in Streamlit
    st.pyplot(fig)


def main():
    """Simple multipage app with Streamlit"""

    # Define a dictionary with all available pages
    pages = {
        "Home": home_page,
        "Insert": insert_page,
        "Results": result_page,
    }

    # Define the sidebar with page selection
    st.sidebar.title("Navigation")
    page_selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page with the page function
    pages[page_selection]()

def home_page():
    """Home page"""
    st.title("WELCOME")
    st.subheader("Convert your Datas into Graphs")
    image = Image.open('ladygraph.jpg')

    st.image(image, caption='DATAS INTO GRAPH',width=500)
    st.subheader(":blue[Graphs and charts are great because they communicate information visually. For this reason, graphs are often used in newspapers, magazines and businesses around the world.Here you can easily convert your datas into graphs.]")
    st.write("Click the insert button to go to the next page.")
    

def insert_page():
    # Set the title and subtitle for the upload page
    st.title("Upload Your File")
    

    # Call the upload_file() function to get a pandas DataFrame from an uploaded CSV or Excel file
    df = upload_file()

    # If a file is uploaded, load the data and switch to the Results page
    if df is not None:
        # Get the column names for the x and y axes
        x_col, y_col = select_columns(df)

        # Save the data and column names as session state
        st.session_state.df = df
        st.session_state.x_col = x_col
        st.session_state.y_col = y_col

        # Switch to the Results page
        st.experimental_set_query_params(page="Results")

    # Display the Submit button
    if st.button("Submit"):
        # Do nothing - the Results page has already been loaded
        pass
        st.write('Kindly click the Result button on the sidebar to view the results')

def result_page():
    # Set the title for the Results page
    st.title("Results")
    if 'df' not in st.session_state:
        st.subheader("Please upload a file to get the results.")
        return
    

    # Get the data and column names from session state
    df = st.session_state.df
    x_col = st.session_state.x_col
    y_col = st.session_state.y_col

    # Display the different charts
    chart_type = st.selectbox('Choose a chart type', ['line graph', 'bar graph', 'pie chart','area chart'], key=hash('chart_type'))

    if chart_type == 'line graph':
        # display line chart
        display_line_chart(df, x_col, y_col)
    elif chart_type == 'bar graph':
        # display bar chart
        display_bar_chart(df, x_col, y_col)
    elif chart_type == 'pie chart':
        # display pie chart
        display_pie_chart(df, x_col, y_col)
    else:
        # display area chart
        display_area_chart(df, x_col, y_col)

def select_columns(df):
    # Display the column selector widget
    st.write("Select the columns for the x and y axes.")
    x_col = st.selectbox("X axis", df.columns)
    y_col = st.selectbox("Y axis", df.columns)

    # Return the column names
    return x_col, y_col



if __name__ == "__main__":
    main()
