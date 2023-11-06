import streamlit as st
from PIL import Image

st.set_page_config(page_title="Air Quality Index Reference Guide", layout="wide", menu_items={"About":"Made by Leinas"})
image = Image.open("Images\AQI_Chart_US.png")
st.image(image=image, caption="United States AQI Reference Guide", width = 1000)