import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import socket

import pandas as pd
from constants import *
import requests
import json
from datetime import datetime, date
from datetime import timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from matplotlib import  pyplot as plt
from io import StringIO
from bse_stock import bse_stock
import numpy as np
from kpi import fit_arima_model

s = requests.session()

ind_name = "S&P BSE 200"
INDEX_SCRIPS["PAYLOAD"]["strfilter"] = ind_name
ind_scrips = s.get(INDEX_SCRIPS["URL"], params=INDEX_SCRIPS["PAYLOAD"], headers=HEADERS)
ind_scrips_data = json.loads(ind_scrips.content.decode('utf-8'))
ind_scrips_df = pd.DataFrame(ind_scrips_data["Table"])
df2 = ind_scrips_df[["scripname","scripname"]]
df2.columns = ["label", "value"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
        html.H1("BSE Stock analysis"),
        style={'height': '3vh', 'marginBottom': '3vh'}
    ),
    html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(
                        id='select_stock',
                        options=df2.to_dict('records'),
                        value='INFY'
                    ),
                    dcc.DatePickerSingle(
                        id='my_date_picker_start',
                        min_date_allowed=date(2019, 1, 1),
                        max_date_allowed=datetime.today(),
                        initial_visible_month=date(2020, 1, 1),
                        date=date(2020,1,1),
                        display_format='DD-MMM-YYYY',
                    ),

                    dcc.DatePickerSingle(
                        id='my_date_picker_end',
                        min_date_allowed=date(2019, 1, 1),
                        max_date_allowed=datetime.today(),
                        initial_visible_month=date.today(),
                        date=date.today(),
                        display_format='DD-MMM-YYYY',
                    ),
                    html.H6("Investment days ☟"),
                        # style={'width': '15%', 'display': 'inline-block','marginLeft':'2vw'}
                    dcc.Slider(
                        id='my-slider',
                        min=0,
                        max=30,
                        step=1,
                        value=10,
                        tooltip={"placement": "bottom", "always_visible": True},
                    ),
                    html.Div(
                        [
                            html.H6("Forecasting"),
                            html.Div(
                                html.H6("P"),
                                style = {'display':'inline-block','vertical-align': 'top'}

                            ),
                            html.Div(
                                dcc.Slider(
                                    id='p-slider',
                                    min=0,
                                    max=30,
                                    step=1,
                                    value=10,
                                    tooltip={"placement": "bottom", "always_visible": True},
                                ),
                                style = {'display':'inline-block','vertical-align': 'top','width':'80%'}
                            )
                        ]
                    ),
                    html.Div(
                        [
                            html.Div(
                                html.H6("D = 0,"),
                                style={'display': 'inline-block', 'vertical-align': 'top', "width":"50%"}
                            ),
                            html.Div(
                                html.H6("Q = 0"),
                                style={'display': 'inline-block', 'vertical-align': 'top', "width":"50%"}

                            )
                        ]
                    ),
                    html.H6("Recommendation"),
                    html.Div(
                        # Insert announcemnt and sentiment analysis results here.
                    )
                ],
                style = {'width':'18%', 'display':'inline-block','vertical-align': 'top'}
            ),
            html.Div(
                dcc.Graph(id="graph_1", style={'width': '82vw', 'height': '90vh'}),
                style = {'width':'82%', 'display':'inline-block','vertical-align': 'top'}
            )
            ]
    )
])

@app.callback(
    Output("graph_1", "figure"),
    [Input("select_stock", "value"),
     Input("my_date_picker_start", "date"),
     Input("my_date_picker_end", "date"),
     Input("my-slider", "value"),
     Input("p-slider", "value")
     ])
def display_candlestick(value,start_date,end_date,n_days,p):
    scripname = value
    if start_date is not None:
        start_ts = str(int(datetime.strptime(start_date,"%Y-%m-%d").timestamp()))
    if end_date is not None:
        end_ts = str(int(datetime.strptime(end_date, "%Y-%m-%d").timestamp()))

    stock_1 = bse_stock(scripname, start_ts, end_ts)
    df = stock_1.get_historic_data()
    df.index = pd.to_datetime(df["Date"])
    df.drop(columns=["Date"], inplace=True)
    fig = make_subplots(rows=2,
                        cols=1,
                        shared_xaxes=True,
                        subplot_titles=(f"Share price of {value}", f"Change in price in {n_days} days"),
                        vertical_spacing=0.05,
                        specs=[[{"secondary_y": False}],
                               [{"secondary_y": True}]]
                        )
    fig.add_trace(
        go.Candlestick(
            name='High-Low',
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Adj Close'],
        ),
        row=1,
        col=1
    )
    fig.add_trace(
        go.Scatter(
            name='Adj Close',
            x=df.index,
            y=df['Adj Close'],
            mode="lines",
            line=dict(
                color="blue"
            )
        ),
        row=1,
        col=1

    )
    df["diff"] = df["Adj Close"].diff(int(n_days))
    df["diff%"] = df["diff"]/df['Adj Close'].shift(periods=n_days) * 100
    # kpi_all = stock_kpi(df)
    st_dt = datetime.strptime(start_date,"%Y-%m-%d")
    ed_dt = datetime.strptime(end_date,"%Y-%m-%d")
    prediction, future = fit_arima_model(df["diff%"].to_frame(), st_dt, ed_dt, n_days=n_days, p=p, d=0, q=0, future=True)
    fig.add_trace(
        go.Bar(x=df.index, y=df['diff'], name=f'Absolute change in Price'),
        row=2,
        col=1,
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            name = '% change in Price',
            x=df.index,
            y=df['diff%'],
            mode="lines",
            line=dict(
                color="black"
            ),
        ),
        row=2,
        col=1,
        secondary_y=True

    )
    if future is None:
        training = prediction.iloc[0:-n_days]
        fig.add_trace(
            go.Scatter(
                name = 'ARIMA training',
                x=training.index,
                y=training['predict'],
                mode="lines",
                line=dict(
                    dash="dash",
                    color="red"
                ),
            ),
            row=2,
            col=1,
            secondary_y=True

        )
        predicted_points = prediction.iloc[-n_days:]
        fig.add_trace(
            go.Scatter(
                name = 'Predicted datapoints',
                x=predicted_points.index,
                y=predicted_points['predict'],
                mode="lines+markers",
                line=dict(
                    # dash="dash",
                    color="blue"
                ),
            ),
            row=2,
            col=1,
            secondary_y=True

        )
    print(future)
    if future is not None:
        fig.add_trace(
            go.Scatter(
                name='ARIMA model',
                x=prediction.index,
                y=prediction['predict'],
                mode="lines",
                line=dict(
                    dash="dash",
                    color="red"
                ),
            ),
            row=2,
            col=1,
            secondary_y=True

        )
        fig.add_trace(
            go.Scatter(
                name='Predicted datapoints',
                x=future.index,
                y=future['predict'],
                mode="lines+markers",
                line=dict(
                    # dash="dash",
                    color="blue"
                ),
            ),
            row=2,
            col=1,
            secondary_y=True

        )
    fig.update_yaxes(title_text="<b>Share price</b> [INR]", secondary_y=False, row=1, col=1)
    fig.update_yaxes(title_text="<b>Change in price</b> [INR]", secondary_y=False, row=2, col=1)
    fig.update_yaxes(title_text="<b>change in price</b> %", secondary_y=True, row=2, col=1)

    fig.update_layout(xaxis_rangeslider_visible=False,
                      margin=dict(l=10, r=30, t=20, b=20),
                      legend=dict(yanchor="top", y=1, xanchor="left", x=0))
    return fig

host = socket.gethostbyname(socket.gethostname())
app.run_server(debug=False,host=host,port=8050)
