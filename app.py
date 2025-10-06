from dotenv import load_dotenv
from openai import OpenAI
import os
import pandas as pd
import streamlit as st

# -- App config
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# -- Set page config
apptitle = 'VictorIA Trekkers'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

st.markdown(
    """
<style>
span[data-baseweb="tag"] {
  color: #07173F !important;
}
</style>
""",
    unsafe_allow_html=True,
)

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

    prompt = st.text_area("Ask a question about the data", "How many rows are in the dataset?")
    if st.button("Get Answer"):
        response = client.chat.completions.create(
            extra_body={},
            model="google/gemma-3-4b-it:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "dataframe",
                            "dataframe": uploaded_df.to_json()
                        }
                    ]
                }
            ]
        )
        st.write("Answer from AI provider:")
        st.write(response.choices[0].message["content"])
