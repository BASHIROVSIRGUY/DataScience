from logging import PlaceHolder
import pandas as pd

import dash
from dash import html
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

import warnings
warnings.filterwarnings("ignore")


def get_zone_list():
    return ['ОБСЛУЖИВАНИЕ УС ','ОТМ','FLM','SLM','Средства','АДМ','ИТ','Все зоны']

def get_bank_list():
    return df['ТБ'].unique()

def get_device_type_list():
    return df['Тип УС'].unique()    

def calc_graph_data_for_regression():
    global df
    df_sub = df[["ДАТА", 'ТБ', 'ОТМ', 'ФРВ', 'Тип УС']]
    df_sub.insert(0, 'ФРВ банка', None)
    df_sub.insert(0, 'ОТМ банка', None)
    df_sub.insert(0, 'ОТМ Красного банка', None)
    for bank_name in df_sub['ТБ'].unique():
        if bank_name == 'Красный банк':
            continue
        for device_type in df_sub['Тип УС'].unique():
            for current_date in df_sub['ДАТА'].unique():

                df_sub.loc[(df_sub['ТБ'] == bank_name) 
                         & (df_sub['ДАТА'] == current_date) 
                         & (df_sub['Тип УС'] == device_type), 'ФРВ банка'] = \
                    int(df_sub[(df_sub['ТБ'] == bank_name) 
                             & (df_sub['ДАТА'] == current_date) 
                             & (df_sub['Тип УС'] == device_type)]['ФРВ'].sum())

                df_sub.loc[(df_sub['ТБ'] == bank_name) 
                         & (df_sub['ДАТА'] == current_date) 
                         & (df_sub['Тип УС'] == device_type), 'ОТМ банка'] = \
                    int(df_sub[(df_sub['ТБ'] == bank_name) 
                             & (df_sub['ДАТА'] == current_date) 
                             & (df_sub['Тип УС'] == device_type)]['ОТМ'].sum())

                df_sub.loc[(df_sub['ТБ'] == bank_name) 
                         & (df_sub['ДАТА'] == current_date) 
                         & (df_sub['Тип УС'] == device_type), 'ОТМ Красного банка'] = \
                    int(df_sub[(df_sub['ТБ'] == 'Красный банк') 
                             & (df_sub['ДАТА'] == current_date) 
                             & (df_sub['Тип УС'] == device_type)]['ОТМ'].sum())

    graph_df = df_sub.drop(['ОТМ', 'ФРВ'], axis=1).drop_duplicates(ignore_index=True).dropna()
    return graph_df

# def color_for_bank_list():
#     color_dict = {
#         'Синий банк':"blue",
#         'Красный банк':"red",
#         'Желтый банк':"yellow",
#         'Черный банк':"black",
#         'Оранжевый банк':"orange",
#         'Серый банк':"grey",
#         'Белый Банк':"white", 
#         'Зеленый банк':"green",
#         'Коричневый банк':"brown",
#         'Золотой банк':"goldenrod",
#         'Бронзовый банк':"#cd7f32",
#     }
#     result_array = []
#     bank_name_list = get_bank_list()
#     for bank_name in bank_name_list:
#         result_array.append(color_dict[bank_name])

#     return result_array

tabs_styles = {
    'height': '44px'
}

tab_style = {
    'borderBottom': '1px solid #1E1E1E',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': 'lightgrey',
    'backgroundColor': 'rgba(50, 50, 50, 0)',
}

tab_selected_style = {
    'borderTop': '1px solid #1E1E1E',
    'borderBottom': '1px solid #1E1E1E',
    'backgroundColor': '#0000ff',
    'color': 'white',
    'padding': '6px'
}

df = pd.read_excel('Приложение №2.xlsx', parse_dates=True)
# external_stylesheets = ['./assets/style.css']
graph_df = calc_graph_data_for_regression()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(style=tabs_styles, children = [
        dcc.Tab(label='Задача 1.1.', style=tab_style, selected_style=tab_selected_style, children = [
            html.Div(className='row', children = [
                html.Div(className='four columns div-user-controls', children = [
                    html.H2('Cтатистика простоя и доступности сети'),
                    html.Div(className='div-for-dropdown', style={'color': '#1E1E1E'}, children=[
                        dcc.RadioItems(
                            id='graph_type_selector',
                            options=['Простой', 'Доступность сети'],
                            value='Простой',
                            style={'color':'#d8d8d8'},
                            inline=True
                        ),
                        html.Br(),
                        dcc.Markdown('''[Наименование банка](/)'''),
                        dcc.Dropdown(
                            id='bank_name_selector', 
                            options=get_bank_list(),
                            multi=True, 
                            value=get_bank_list(),
                            style={'backgroundColor': '#1E1E1E'},
                            className='bank_name_selector'
                        ),
                        html.Br(),
                        dcc.Markdown('''[Зоны](/)'''),
                        dcc.RadioItems(
                            id='zone_selector',
                            options=get_zone_list(),
                            value="Все зоны",
                            style={'color':'#d8d8d8'}
                        ),
                        html.Br(),
                        dcc.Markdown('''[Тип устройства](/)'''),
                        dcc.Checklist(
                            id='type_device_selector',
                            options=get_device_type_list(),
                            value=get_device_type_list(), 
                            style={'color':'#d8d8d8'}
                        )
                    ])
                ]),
                html.Div(className='eight columns div-for-charts bg-grey', children=[
                    dcc.Loading(
                        dcc.Graph(id='daily_statistics_graph'),
                        type="cube"
                    ),
                    html.Label("Число", htmlFor='date_range_slider', title="Числа месяца"),
                    dcc.RangeSlider(1, 31, 1, value=[1, 15], id='date_range_slider')
                ])
            ])
        ]),
        dcc.Tab(label='Задача 1.2.', style=tab_style, selected_style=tab_selected_style, children=[
            html.Div(className='row', children=[
                html.Div(className='four columns div-user-controls', children=[
                    html.H2('Выявление зависимости от Красного банка'),
                    html.Br(),
                    html.Button('Обновить', id='submit_botton', style={'margin-left': '40px', 'margin-top': '10px'}),
                ]),
                html.Div(className='eight columns div-for-charts bg-grey', children=[
                    dcc.Loading(
                        dcc.Graph(id='regression_graph', animate=True),
                        type="cube"
                    ),
                ]),
            ])
        ])
    ])
])



@app.callback(Output('daily_statistics_graph', 'figure'),
             [Input('graph_type_selector', 'value'),
              Input('bank_name_selector', 'value'),
              Input('zone_selector', 'value'),
              Input('type_device_selector', 'value'),
              Input('date_range_slider', 'value')])
def update_graph_one(type_graph, bank_name_list, zone_name, type_list, range_period):
    global df
    # df = pd.read_excel('Приложение №2.xlsx', parse_dates=True)
    df_sub = df[(df['ТБ'].isin(bank_name_list))
              & (df['Тип УС'].isin(type_list))
              & (df['День'] >= range_period[0]) & (df['День'] <= range_period[1])]

    def get_zone_tag(zone_name):
        if zone_name == 'Все зоны':
            return "Простой"
        else:
            return zone_name

    if type_graph == 'Простой':
    
        fig = px.strip(df_sub,
                    x="ТБ", y=get_zone_tag(zone_name),
                    color="Тип УС",
                    hover_name="ДАТА",
                    template='plotly_dark',
                    hover_data=["Средства", "ФРВ"])

    elif type_graph == 'Доступность сети':

        df_sub.insert(0, 'Доступность сети', None)
        df_sub.loc[(df_sub['ФРВ'] > 0), 'Доступность сети'] = df_sub[(df_sub['ФРВ'] > 0)]['Простой'] / df_sub[(df_sub['ФРВ'] > 0)]['ФРВ']
        # df_sub = df_sub.dropna()
        df_sub[:]['Доступность сети'] = df_sub['Доступность сети'] * 100
        
        fig = px.strip(df_sub,
                    x="ТБ", y="Доступность сети",
                    color="Тип УС",
                    hover_name="ДАТА",
                    template='plotly_dark',
                    hover_data=["Средства", "ФРВ"])
    
    return fig



@app.callback(Output('regression_graph', 'figure'),
              [Input('submit_botton', 'n_clicks')])
def update_graph_two(n):
    # graph_df = calc_graph_data_for_regression()
    global graph_df

    fig = px.scatter(graph_df, 
                     x='ОТМ Красного банка', y='ОТМ банка', 
                     hover_name="ДАТА",
                     size=list(graph_df['ФРВ банка'].values),
                     hover_data=['ФРВ банка'],
                     size_max=14,
                     color="Тип УС",
                     template='plotly_dark',
                     symbol="Тип УС",
                     facet_col="ТБ", facet_col_wrap=2, 
                     trendline="ols")

    fig.update_layout(
        height=100*n + 800
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)