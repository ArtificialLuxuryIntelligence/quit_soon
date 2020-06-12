from datetime import time as t
from datetime import datetime as dt
from datetime import date as dtdate
import json

from django.contrib.auth.models import User
from django_plotly_dash import DjangoDash

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from . import DataFrameDate


with open('user_dict.txt') as json_file:
    user_dict = json.load(json_file)
    i=0
    for p in user_dict['date']:
        user_dict['date'][i] = dt.strptime(p, '%Y-%m-%d')
        i += 1
    i=0
    for p in user_dict['money_smoked']:
        user_dict['money_smoked'][i] = float(user_dict['money_smoked'][i])
        i += 1

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('ConsoCigGraph', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.RadioItems(id='my-radio',
                 options=[
                    {'label': 'Jour', 'value':'D'},
                    {'label': 'Semaine', 'value':'W'},
                    {'label': 'Mois', 'value':'M'},
                 ],
                 value='D',
                 labelStyle={'display': 'inline-block'}
                 ),
    dcc.Checklist(id='my-checkbox',
        options=[{'label': 'Voir mes activités saines', 'value': 'A'},],
        # value=['MTL', 'SF'],
        ),
    dcc.Graph(id='graph',
              animate=False,
              style={"backgroundColor": "#1a2d46", 'color': '#ffffff'},
              ),
    dcc.Graph(id='graph2',
              animate=False,
              style={"backgroundColor": "#1a2d46", 'color': '#ffffff'},
              ),
])

def fig(df, checkbox, fig_name, bar_name, y_name, y_data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=df.index, y=y_data, name=bar_name),
        secondary_y=False,
        )

    if checkbox :
        fig.add_trace(
            go.Scatter(x=df.index, y=df.activity_duration, name="Activités saines", mode='lines'),
            secondary_y=True,
        )

    fig.update_layout(
        title_text=fig_name,
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        )
    # Set x-axis title
    fig.update_xaxes(title_text="Dates")

    # Set y-axes titles
    fig.update_yaxes(title_text=y_name,
                     range=[0, max(y_data)],
                     secondary_y=False,
                     dtick=1,
                     showgrid=False,
                     zeroline=False,
                     showline=False,)
    fig.update_yaxes(title_text="Activités (en minutes)",
                     range=[0, max(df.activity_duration)],
                     secondary_y=True,
                     dtick=15,
                     showgrid=False,
                     zeroline=False,
                     showline=False,)
    return fig

def dataframe(radio):
    df = DataFrameDate(user_dict)
    if radio == 'D':
        df = df.day_df
    elif radio == 'W':
        df = df.week_df
    elif radio == 'M':
        df = df.month_df
    return df

@app.callback(
    Output('graph', 'figure'),
    [Input('my-radio', 'value'), Input('my-checkbox', 'value')],
)
def display_value(radio, checkbox):
    df = dataframe(radio)
    fig1 = fig(df, checkbox, "Consommation de cigarettes", "Conso cigarette", "Cigarettes", df.nb_cig)
    return fig1

@app.callback(
    Output('graph2', 'figure'),
    [Input('my-radio', 'value'), Input('my-checkbox', 'value')],
)
def display_value(radio, checkbox):
    df = dataframe(radio)
    fig2 = fig(df, checkbox, "Agent parti en fumée", "Argent dépensé (en€)", "Cigarettes", df.money_smoked)
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)
