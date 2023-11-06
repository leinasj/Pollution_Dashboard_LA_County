import folium

m=folium.Map([34.0756, -118.3],zoom_start=10)

folium.Marker(
    location=[34.0663, -118.227],
    tooltip="Monitor 1",
    popup="Central LA CO",
    icon=folium.Icon(icon="cloud", color = 'blue'),
).add_to(m)

folium.Marker(
    location=[33.9288,-118.211],
    tooltip="Monitor 2",
    popup="S Central LA CO",
    icon=folium.Icon(icon="cloud", color = 'blue'),
).add_to(m)

folium.Marker(
    location=[34.0102,-118.069],
    tooltip="Monitor 3",
    popup="S San Gabriel Vly",
    icon=folium.Icon(icon="cloud", color = 'blue'),
).add_to(m)

folium.Marker(
    location=[33.9883,-118.47],
    tooltip="Monitor 4",
    popup="NW Coastal LA",
    icon=folium.Icon(icon="cloud", color = 'blue'),
).add_to(m)

folium.Marker(
    location=[33.8604,-118.144],
    tooltip="Monitor 5",
    popup="S Coastal LA",
    icon=folium.Icon(icon="cloud", color = 'blue'),
).add_to(m)

folium.Marker(
    location=[33.7934,-118.316],
    tooltip="Monitor 6",
    popup="SW Coastal LA",
    icon=folium.Icon(icon="cloud", color = 'blue'),
).add_to(m)

folium.Marker(
    location=[34.2085,-118.202],
    tooltip="Monitor 7",
    popup="W San Gabriel Vly",
    icon=folium.Icon(icon="cloud", color = 'blue'),
).add_to(m)

m.save("map.html")