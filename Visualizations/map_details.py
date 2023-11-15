import folium

color_map = {
    "Good":'green',
    "Moderate": 'yellow',
    "Unhealthy for Sensitive Groups": 'orange',
    "Unhealthy": 'red',
    "Very Unhealthy": 'purple',
    "Hazardous": 'maroon'
}

def define_map(observations):
    m=folium.Map([34, -118.3],zoom_start=10)
    for i, v in observations.iterrows():
        folium.Marker(
            location=[v['Latitude'], v['Longitude']],
            tooltip=f"<b>{v['City']}, AQI: {v['AQI']}, AQI_Classification: {v['AQI_Classification']}</b>",
            popup=folium.Popup(folium.IFrame(
                f"<b>AQI (Ozone):</b> {v['AQI']}<br><b>AQI_Classification:</b> {v['AQI_Classification']}<br><b>Last Observation at:</b> {v['HourObserved']}:00 {v['LocalTimeZone']}, {v['Date'].isoformat()}<br><b>Monitor Site:</b> {v['City']}<br><b>Coordinates:</b> {v['Longitude'],v['Latitude']}"),
            min_width=310, max_width=310, parse_html = True),
            icon=folium.Icon(icon="cloud", color = f"{color_map[v['AQI_Classification']]}"),
        ).add_to(m)

    m.save("map.html")