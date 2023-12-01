import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def plot_ts(mid_point, x, title, chart_type={'line', 'bar', 'scatter'}):
    if chart_type == "line":
        # Plot Time Series
        fig = px.line(x.sort_values('Date'), x = "Date", y ="AQI", color = "City", title = title)
        fig2 = px.scatter(x.sort_values('Date'), x = "Date", y ="AQI")

        fig = go.Figure(data=fig.data + fig2.data)
        fig.update_layout(title = title,xaxis_title="Date", yaxis_title="AQI")
    if chart_type == "bar":
        # Plot Time Series
        fig = px.bar(x.sort_values('Date'), x = "Date", y ="AQI", color = "City", title = title, barmode='group',)
    
    if chart_type == "scatter":
        for i in x['Date'].unique():
            for j in x['City'].unique():
                x.loc[(x['Date']==i) & (x['City']==j), 'e'] = np.std(x.loc[(x['Date']==i) & (x['City']==j)]['AQI'])
                x.loc[(x['Date']==i) & (x['City']==j), 'avg'] = np.mean(x.loc[(x['Date']==i) & (x['City']==j)]['AQI'])
        fig = px.scatter(x.sort_values('Date'), x="Date", y="avg", color="City", error_y="e")
        fig.update_traces(showlegend=False)
        fig2 = px.line(x.sort_values('Date'), x="Date", y="avg", color = "City")
        fig = go.Figure(data=fig.data + fig2.data)
        fig.update_layout(title = title,xaxis_title="Date", yaxis_title="AQI")
        fig.update_xaxes(tickformat="%Y-%m-%d")
    # AQI Classification lines for reference points of AQI values
    if max(x['AQI']) >= 0 and max(x['AQI']) <= 75:
        fig.add_hline(y=50, line_width=3, line_dash="dash", line_color="green")
        fig.add_annotation(x=mid_point, y=47.5, text="Good", showarrow = False)
    elif max(x['AQI']) >= 75:
        fig.add_hline(y=50, line_width=3, line_dash="dash", line_color="green")
        fig.add_annotation(x=mid_point, y=25, text="Good", showarrow = False)
        fig.add_annotation(x=mid_point, y=75, text="Moderate", showarrow = False)
        fig.add_hline(y=100, line_width=3, line_dash="dash", line_color="yellow")
    if max(x['AQI']) >=100:
        fig.add_annotation(x=mid_point, y=125, text="Unhealthy for Sensitive Groups", showarrow = False)
        fig.add_hline(y=150, line_width=3, line_dash="dash", line_color="orange")
    if max(x['AQI']) >=150:
        fig.add_annotation(x=mid_point, y=175, text="Unhealthy", showarrow = False)
        fig.add_hline(y=200, line_width=3, line_dash="dash", line_color="red")
        fig.add_annotation(x=mid_point, y=210, text="Very Unhealthy/Hazardous", showarrow = False)

    return fig

