import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="Los Angeles County Air Pollutants 2000-Present", layout="wide", menu_items={"About":"Made by Leinas"})
st.markdown("<h1 style='text-align: center;'>Los Angeles County Air Pollutants (2000-Present)</h1>", unsafe_allow_html=True)
st.sidebar.header("Dashboard Options")

HtmlFile = open("Images\map.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, width=1300, height=500)