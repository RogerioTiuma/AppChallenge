import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import requests, os
from gwpy.timeseries import TimeSeries
from gwosc.locate import get_urls
from gwosc import datasets
from gwosc.api import fetch_event_json

from copy import deepcopy
import base64

from helper import make_audio_file

# Use the non-interactive Agg backend, which is recommended as a
# thread-safe backend.
# See https://matplotlib.org/3.3.2/faq/howto_faq.html#working-with-threads.
import matplotlib as mpl

mpl.use("agg")

##############################################################################
# Workaround for the limited multi-threading support in matplotlib.
# Per the docs, we will avoid using `matplotlib.pyplot` for figures:
# https://matplotlib.org/3.3.2/faq/howto_faq.html#how-to-use-matplotlib-in-a-web-application-server.
# Moreover, we will guard all operations on the figure instances by the
# class-level lock in the Agg backend.
##############################################################################
from matplotlib.backends.backend_agg import RendererAgg
from threading import Lock

_lock = Lock()

# -- Set page config
apptitle = 'VictorIA Trekkers'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

st.sidebar.image("assets/image2.png", use_column_width=True)
st.sidebar.markdown("# Exoplanet Data Explorer")

uploaded_df = None
with st.sidebar:
    tab_input, tab_view = st.tabs(["Input", "View"])
    with tab_input:
        # -- upload data file
        tab_input.markdown('## Data load')
        uploaded_file = tab_input.file_uploader("Choose an Excel or CSV file", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            # Check file type and load accordingly
            if uploaded_file.name.endswith('.csv'):
                uploaded_df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                uploaded_df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file type.")
                uploaded_df = None

        tab_input.markdown('## AI configuration')
        tab_input.markdown('### Model')
        select_model = tab_input.selectbox('Select Model', ['None', 'CNN', 'CNN + Explainability Layer', 'SNN', 'GAN',
                                                             'KNN', 'RF', 'DT', 'CatBoost', 'Logistic Regression'])

        tab_input.markdown('### Set hyperparameters')
        test_size = tab_input.slider('Test size (%)', 0, 100, 30)  # min, max, default
        max_iter = tab_input.slider('Max iterations', 100, 5000, 1000)  # min, max, default
        random_state = tab_input.slider('Random state', 10, 100, 42)  # min, max, default
        validation_fraction = tab_input.slider('Validation fraction', 0, 20, 15)  # min, max, default

        data_origin = tab_input.multiselect('Select Data Origin', ['Kepler', 'K2', 'TESS'])

        # Display the uploaded data for preview in main area
        if uploaded_df is not None:
            # Append button
            if st.button("Append to Main DataFrame"):
                # Append uploaded data to main dataframe
                st.session_state["main_df"] = pd.concat(
                    [st.session_state["main_df"], uploaded_df], ignore_index=True
                )
                st.success("Data appended!")

    with tab_view:
        st.write("Data Preview")
        if uploaded_file is not None and uploaded_df is not None:
            st.dataframe(uploaded_df)
        else:
            st.write("No data uploaded yet.")

st.title("Main Content Area")
if uploaded_df is not None:
    st.write("Preview of uploaded data:")
    st.dataframe(uploaded_df)
