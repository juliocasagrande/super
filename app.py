import dash
from dash import dcc,html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

load_figure_template('darkly')

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY]
)
server = app.server

#Ingestão de dados
df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])

#Layout
app.layout = html.Div(children=[

    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H4('Supermercados'),
                html.H2('Casagrande'),
                html.Hr(),
                html.H6('Esse é um dashboard de vendas de supermercado feito pelo Júlio Casagrande'),
                html.H4('Cidades:'),
                dcc.Checklist(np.unique(df_data['City']),
                np.unique(df_data['City']), id='check_city', inputStyle={'margin-right':'5px','margin-left':'10px'}),
                html.H4('Variável de análise:', style={'margin-top':'15px'}),
                dcc.RadioItems(['gross income','Rating'],'gross income',id='main_variable',
                inputStyle={'margin-right':'5px','margin-left':'10px'}),
            ], style={'height':'92vh','margin':'20px','padding':'10px'})
        ], sm=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id='city_fig')], sm=4),
                dbc.Col([dcc.Graph(id='gender_fig')], sm=4),
                dbc.Col([dcc.Graph(id='pay_fig')], sm=4)
            ]),
            dbc.Row([dcc.Graph(id='income_per_date_fig')]),

            dbc.Row([dcc.Graph(id='income_per_product_fig')])

        ], style={'margin-top':'20px'}, sm=10)
    ])
])

#Callbacks
@app.callback([
    Output('city_fig', 'figure'),
    Output('pay_fig', 'figure'),
    Output('gender_fig', 'figure'),
    Output('income_per_date_fig', 'figure'),
    Output('income_per_product_fig', 'figure')],
    
    [
        Input('check_city', 'value'),
        Input('main_variable', 'value')
    ])
def render_graphs(cities, main_variable):

    operation = np.sum if main_variable == "gross income" else np.mean

    df_filtered = df_data[df_data['City'].isin(cities)]

    df_city = df_filtered.groupby('City')[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby('Payment')[main_variable].apply(operation).to_frame().reset_index()
    df_gender = df_filtered.groupby(['Gender','City'])[main_variable].apply(operation).to_frame().reset_index()
    df_income_per_product = df_filtered.groupby(['Product line','City'])[main_variable].apply(operation).to_frame().reset_index()
    df_income_per_date = df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city,x='City',y=main_variable)
    fig_payment = px.bar(df_payment,y='Payment',x=main_variable, orientation='h')
    fig_gender = px.bar(df_gender,x='Gender',y=main_variable, color='City', barmode='group')
    fig_income_per_product = px.bar(df_income_per_product,x=main_variable,y='Product line', color='City', orientation='h', barmode='group')
    fig_income_per_date = px.bar(df_income_per_date,y=main_variable,x='Date')
    
    fig_city.update_layout(margin=dict(l=0, r=0, t=50, b=20), height=200, template='darkly',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_payment.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template='darkly',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_gender.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template='darkly',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_income_per_product.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500, template='darkly',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0, 0, 0, 0)')
    fig_income_per_date.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=190, template='darkly',plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0, 0, 0, 0)')

    return fig_city, fig_payment, fig_gender, fig_income_per_product, fig_income_per_date

#Servidor
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)