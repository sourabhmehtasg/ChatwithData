import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from PIL import Image
import numpy as np


# App config
st.set_page_config(
    page_title="Data GPT",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded"
)

col1, col2, col3 = st.columns(3)
with col2:
    st.header('🤖  DataGPT')


st.subheader(" 📄 Upload your excel file", divider='rainbow')
df = pd.DataFrame()
uploaded_file = st.file_uploader("Choose a EXCEL file", label_visibility="hidden")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    df = pd.DataFrame({
        "country": ["United States", "United Kingdom", "France", "Germany", "Italy", "Spain", "Canada", "Australia", "Japan", "China"],
        "gdp": [19294482071552, 2891615567872, 2411255037952, 3435817336832, 1745433788416, 1181205135360, 1607402389504, 1490967855104, 4380756541440, 14631844184064],
        "happiness_index": [6.94, 7.16, 6.66, 7.07, 6.38, 6.4, 7.23, 7.22, 5.87, 5.12]
    })

st.write(df)
st.divider()

st.subheader(" ⌨️ Ask your data", divider='rainbow')

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")


st.write("Enter your query below and submit")
query = st.text_input('Enter your query', value="", label_visibility="hidden")
submitted = st.button("Submit")
if submitted:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    else:
        if len(query) > 0:
            with st.spinner(text="Fetching your result..."):
                llm = OpenAI(api_token=openai_api_key)

                smart_dataframe = SmartDataframe(df, config={"llm": llm})
                answer_frame = smart_dataframe.chat(str(query))
                # chart_frame = smart_dataframe.chat("Plot the bar chart for "+str(query))

            st.success("Here is the result for:    "+query, icon="✅")

            if isinstance(answer_frame,SmartDataframe):
                st.write(answer_frame.reset_index(drop=True))
            elif isinstance(answer_frame,str):
                msg = str(answer_frame)
                st.markdown("### "+msg)
            elif isinstance(answer_frame,np.int64):
                msg = '{:,.2f}'.format(answer_frame)
                st.markdown("### "+msg)
            elif isinstance(answer_frame,np.float64):
                msg = '{:,.2f}'.format(answer_frame)
                st.markdown("### "+msg)
            else:
                msg = '{:,.2f}'.format(answer_frame)
                st.markdown("### "+msg)   
        else:
            st.error('Query input can not be empty, type in your question and press Submit button !!', icon="🚨")

