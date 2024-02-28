import streamlit as st
import pandas as pd
from utils import get_google_trends_data
from pytrends.exceptions import TooManyRequestsError
import time
st.title('Analista de Google Trends')

# Input keyword from user
keyword = st.text_input("Enter a keyword to search on Google Trends", "Python")

# Get data for the keyword
try:
    data = get_google_trends_data(keyword)

    # Display the data
    st.subheader('Google Trends Data')
    st.write(data)
except TooManyRequestsError:
    st.error("Too many requests. Please wait and try again later.")


