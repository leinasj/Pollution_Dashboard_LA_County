import streamlit as st
from PIL import Image

st.set_page_config(page_title="Air Quality Index Reference Guide", layout="wide", menu_items={"About":"Made by Leinas"})
st.markdown("<h1 style='text-align: left;'>Air Quality Index (AQI)</h1>", unsafe_allow_html=True)
st.divider()
st.markdown("<b style='text-align: left;'>The EPA developed the AQI, which reports levels of ozone, particle pollution, and other common air pollutants on the same scale. An AQI reading of 101 corresponds to a level above the national air quality standard - the higher the AQI rating, the greater the health impact.</b>", unsafe_allow_html=True)
image = Image.open("Visualizations\AQI_Chart_US.png")
st.image(image=image, caption="United States AQI Reference Guide", width = 1000)
st.divider()
st.markdown("<h1 style='text-align: left;'>Air quality observations</h1>", unsafe_allow_html=True)
st.markdown("<b style='text-align: left;'>Hourly or daily observations are measured and reported to AirNow by federal, state, local, and tribal air quality agencies. Historical (daily) AQI values are calculated using an averaging method, and real-time AQI values are based on a NowCast calculation. This dashboard tracks current AQI reports per 3 hour intervals from 6 different monitoring sites in the Los Angeles County area.</b>", unsafe_allow_html=True)
st.divider()
st.markdown("<h1 style='text-align: left;'>Action Days</h1>", unsafe_allow_html=True)
st.markdown("<b style='text-align: left;'>Action days are usually called when the AQI reaches unhealthy or higher. Different air pollution control agencies call Action Days at different levels. In some places, action days are called when the AQI is forecast to be Unhealthy for Sensitive Groups, or Code Orange. In this case, the groups that are sensitive to the pollutant should reduce exposure by eliminating prolonged or heavy exertion outdoors. For ozone this includes children and adults who are active outdoors and people with lung disease, such as asthma. For particle pollution this includes: people with heart or lung disease, older adults and children.</b>", unsafe_allow_html=True)