import pandas as pd
import plotly.express as px
import plotly.io as poi
import dash
from dash import dcc
from dash import html
poi.renderers.default = 'browser'
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 
import os
# IMPORTS OVER

#PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "games.csv")
#PATH


# PRESETTING DATA
df = pd.read_csv(file_path)
df.dropna(inplace = True)
df = df[df['User_Score'] != 'tbd']
df.Year_of_Release = df.Year_of_Release.astype(int)
df = df.query('Year_of_Release > 2000 and Year_of_Release < 2022')
df['User_Score'] = df['User_Score'].astype(float)
df['Critic_Score'] = df['Critic_Score'].astype(float)
df_1 = pd.DataFrame({'Rating':['E', 'M', 'T', 'E10+', 'AO', 'RP'],'Age_restriction':[0,17,13,10,18, None]})
df = df.merge(df_1, how='left', on = 'Rating')
# PRESETTING DATA


# Фильтр 1 - выбор платформ
filter_1 = dcc.Dropdown(id = 'fil_1',
                        options = df.Platform.unique(),
                        multi = True)
# Фильтр 1 - выбор платформ

# Фильтр 2 - выбор жанров
filter_2 = dcc.Dropdown(id = 'fil_2',
                        options = df.Genre.unique(),
                        multi= True
                        )
# Фильтр 2 - выбор жанров

# Фильтр 3 - выбор годов
filter_3 = dcc.RangeSlider(id = 'fil_3', 
                           min = df['Year_of_Release'].min(),
                           max = df['Year_of_Release'].max(),
                           marks = {2001:'2001',2005:'2005',2010:'2010',2016:'2016'},
                           step = 1,
                           value = [2001,2016])
# Фильтр 3 - выбор годов

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# BODY SITE
####
app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1('Дашборд по игровой индустрии'), style={'margin-left':'40px','margin-top':'40px'})),
    dbc.Row(dbc.Col(html.H4('Портфолио data analisys. Дашборд предназначен для оценки истории игровой индустрии по основным \
                    показателям. Дашборд является интерактивным, все графики взаимосвязаны и показывают целостную картину \
                    исходя из выбранных фильтров.'), style={'margin-left':'40px','margin-top':'10px', 'margin-right':'40px'})),
    dbc.Row(dbc.Col(html.H5('Ответственный: Кондауров Валерий. Дата и время обновления данных: по необходимости'),style={'margin-left':'40px', 'margin-right':'40px'})),
    dbc.Row([
        dbc.Col(
            dbc.Row([html.Div("Фильтр выбора платформ",style = {'width':'400px', 'margin-left':'40px'}),
                     html.Div(filter_1,style = {'width':'400px', 'margin-left':'40px','margin-top':'20px'})])),
        dbc.Col(
            dbc.Row([html.Div('Фильтр выбора жанра игр',style = {'width':'400px','margin-left':'35px'}),
                     html.Div(filter_2,style = {'width':'400px','margin-left':'35px','margin-top':'20px'})])),
        dbc.Col(
            dbc.Row([html.Div('Фильтр выбора годов выпуска',style = {'width':'500px','margin-right':'30px'}),
                     html.Div(filter_3,style = {'width':'500px','margin-right':'30px','margin-top':'20px'})])),
    ], style = {'margin-top':'30px'}),
    dbc.Row([
        dbc.Col(
            dbc.Row([html.Div('Общее количество выпущенных игр', style={'textAlign':'center'}),
                     html.H1(id='Figure_1', style={'textAlign':'center','margin-top':'20px'})])),
        dbc.Col(
            dbc.Row([html.Div('Общая средняя оценка критиков', style={'textAlign':'center'}),
                     html.H1(id='Figure_2', style={'textAlign':'center', 'margin-top':'20px'})])),
        dbc.Col(
            dbc.Row([html.Div('Общая средняя оценка игроков', style={'textAlign':'center'}),
                     html.H1(id='Figure_3', style={'textAlign':'center','margin-top':'20px'})]))
    ], style = {'margin-top':'100px',
                'margin_bottom':'200px'}
    ),
    dbc.Row([
        dbc.Col(
            dbc.Row([html.Div('Выпуск игр по годам и платформам', style={'textAlign':'center', 'margin-top':'10px'}),
                     dcc.Graph(id='Figure_4',
                                 style = {'width':'500px'})])),
        dbc.Col(
            dbc.Row([html.Div('Диаграмма рассеяния оценок по жанру', style={'textAlign':'center', 'margin-top':'10px'}),
                     dcc.Graph(id='Figure_5',
                                 style = {'width':'500px'})])),
        dbc.Col(
            dbc.Row([html.Div('График среднего возрастного рейтинга по жанру', style={'textAlign':'center', 'margin-top':'10px'}),
                    dcc.Graph(id='Figure_6',
                                 style = {'width':'500px'})])),
    ], style={'margin-top':'20px'})
],
style = {'margin-left':'60px',
         'margin-right':'60px',
         'border':'1px solid black',
         'margin-top':'5px'})     
# BODY SITE

# SETTING FIGURE 5
@app.callback(
    Output(component_id = 'Figure_5', component_property='figure'),
    [Input(component_id = 'fil_3', component_property = 'value'),
     Input(component_id = 'fil_2', component_property = 'value'),
     Input(component_id = 'fil_1', component_property = 'value')]
    )

def update_dist_temp_chart(filter_3_value,filter_2_value, filter_1_value):
    if filter_1_value is None:
        filter_1_value = []
    if filter_2_value is None:
        filter_2_value = []
    if (filter_2_value != []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value)) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_2_value == []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_1_value == []) & (filter_2_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value))]
    else:
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1])]
    fig_5 = px.scatter(chart_data, x='User_Score',y='Critic_Score',
                   color = 'Genre', 
                   labels = {'Critic_Score':'Оценки игроков',
                             'User_Score':'Оценки критиков',
                             'Genre':'Жанр'})
    return fig_5
# SETTING FIGURE 5

# SETTING FIGURE 1
@app.callback(
    Output(component_id = 'Figure_1', component_property='children'),
    [Input(component_id = 'fil_3', component_property = 'value'),
     Input(component_id = 'fil_2', component_property = 'value'),
     Input(component_id = 'fil_1', component_property = 'value')]
    )

def update_graph_1(filter_3_value,filter_2_value, filter_1_value):
    if filter_1_value is None:
        filter_1_value = []
    if filter_2_value is None:
        filter_2_value = []
    if (filter_2_value != []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value)) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_2_value == []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_1_value == []) & (filter_2_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value))]
    else:
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1])]
    fig_1 = chart_data['Name'].nunique()  
    return fig_1
# SETTING FIGURE 1

# SETTING FIGURE 2
@app.callback(
    Output(component_id = 'Figure_2', component_property='children'),
    [Input(component_id = 'fil_3', component_property = 'value'),
     Input(component_id = 'fil_2', component_property = 'value'),
     Input(component_id = 'fil_1', component_property = 'value')]
    )

def update_graph_2(filter_3_value,filter_2_value, filter_1_value):
    if filter_1_value is None:
        filter_1_value = []
    if filter_2_value is None:
        filter_2_value = []
    if (filter_2_value != []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value)) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_2_value == []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_1_value == []) & (filter_2_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value))]
    else:
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1])]
    fig_2 = round(chart_data['User_Score'].mean(),2)
    return fig_2
# SETTING FIGURE 2

# SETTING FIGURE 3
@app.callback(
    Output(component_id = 'Figure_3', component_property='children'),
    [Input(component_id = 'fil_3', component_property = 'value'),
     Input(component_id = 'fil_2', component_property = 'value'),
     Input(component_id = 'fil_1', component_property = 'value')]
    )

def update_graph_3(filter_3_value,filter_2_value, filter_1_value):
    if filter_1_value is None:
        filter_1_value = []
    if filter_2_value is None:
        filter_2_value = []
    if (filter_2_value != []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value)) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_2_value == []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_1_value == []) & (filter_2_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value))]
    else:
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1])]
    fig_3 = round(chart_data['Critic_Score'].mean(),2)
    return fig_3
# SETTING FIGURE 3

# SETTING FIGURE 4
@app.callback(
    Output(component_id = 'Figure_4', component_property='figure'),
    [Input(component_id = 'fil_3', component_property = 'value'),
     Input(component_id = 'fil_2', component_property = 'value'),
     Input(component_id = 'fil_1', component_property = 'value')]
    )

def update_graph_4(filter_3_value,filter_2_value, filter_1_value):
    if filter_1_value is None:
        filter_1_value = []
    if filter_2_value is None:
        filter_2_value = []
    if (filter_2_value != []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value)) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_2_value == []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_1_value == []) & (filter_2_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value))]
    else:
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1])]
    chart_data['Year_of_Release'] = pd.to_datetime(chart_data['Year_of_Release'],format='%Y')
    chart_data = chart_data.groupby(['Year_of_Release','Platform']).count().reset_index()
    fig_4 = px.area(chart_data, x='Year_of_Release',y='Platform',
                   color = 'Platform', 
                   labels = {'Year_of_Release':'Год выпуска игр',
                             'Platform':'Платформа'})
    return fig_4
# SETTING FIGURE 4

# SETTING FIGURE 6
@app.callback(
    Output(component_id = 'Figure_6', component_property='figure'),
    [Input(component_id = 'fil_3', component_property = 'value'),
     Input(component_id = 'fil_2', component_property = 'value'),
     Input(component_id = 'fil_1', component_property = 'value')]
    )

def update_graph_6(filter_3_value,filter_2_value, filter_1_value):
    if filter_1_value is None:
        filter_1_value = []
    if filter_2_value is None:
        filter_2_value = []
    if (filter_2_value != []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value)) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_2_value == []) & (filter_1_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Platform'].isin(filter_1_value))]
    elif (filter_1_value == []) & (filter_2_value != []):
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1]) &
                        (df['Genre'].isin(filter_2_value))]
    else:
        chart_data = df[(df['Year_of_Release'] >= filter_3_value[0]) & 
                        (df['Year_of_Release'] <= filter_3_value[1])]
    chart_data = chart_data[['Genre','Age_restriction']].groupby('Genre').mean().reset_index().sort_values('Age_restriction')
    fig_6 = px.bar(chart_data, x='Genre',y='Age_restriction', 
                   labels = {'Genre':'Жанры игр',
                             'Age_restriction':'Средний возрастной рейтинг'},
                    text_auto= True)
    return fig_6
# SETTING FIGURE 6

# START SITE
if __name__ == '__main__':
    app.run_server(debug=True)

