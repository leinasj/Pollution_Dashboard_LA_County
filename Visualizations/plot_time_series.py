import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_ts(mid_point, x, title, chart_type={'line', 'bar'}):
    if chart_type == "line":
        # Plot Time Series
        fig = px.line(x.sort_values('Date'), x = "Date", y ="AQI", color = "City", title = title)
        fig2 = px.scatter(x.sort_values('Date'), x = "Date", y ="AQI")

        fig = go.Figure(data=fig.data + fig2.data)
    if chart_type == "bar":
        # Plot Time Series
        fig = px.bar(x.sort_values('Date'), x = "Date", y ="AQI", color = "City", title = title, barmode='group',)
    # AQI Classification lines for reference points of AQI values
    fig.add_hline(y=50, line_width=3, line_dash="dash", line_color="green")
    fig.add_hline(y=100, line_width=3, line_dash="dash", line_color="yellow")
    fig.add_hline(y=150, line_width=3, line_dash="dash", line_color="orange")
    fig.add_hline(y=200, line_width=3, line_dash="dash", line_color="red")
    fig.add_annotation(x=mid_point, y=25, text="Good", showarrow = False)
    fig.add_annotation(x=mid_point, y=75, text="Moderate", showarrow = False)
    fig.add_annotation(x=mid_point, y=125, text="Unhealthy for Sensitive Groups", showarrow = False)
    fig.add_annotation(x=mid_point, y=175, text="Unhealthy", showarrow = False)
    fig.add_annotation(x=mid_point, y=210, text="Very Unhealthy/Hazardous", showarrow = False)
    return fig

