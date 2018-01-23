#use anaconda to run app
#anaconda-on

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

import mysql.connector as sql

#local import
#ensure __init__.py is present in dir.
from conn import conn_str
# conn_str is a dict with the following:
# 'host' : 'yourhostname'
# 'db' : 'yourdbname'
# 'uid' : 'yourusername'
# 'pwd' : 'yourpassword'

#Fetch data from the server
#keep the connection details somewhere safe on the server side.
db_conn = sql.connect(hostname=conn_str['host'],
                      database=conn_str['db'],
                      username=conn_str['uid'],
                      password=conn_str['pwd'])
df = pd.read_sql('SELECT * FROM generic_sensor_data', db_conn)
db_conn.close()


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children = '''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1,2,3], 'y': [4,1,2], 'type': 'bar', 'name':'SF'},
                {'x': [1,2,3], 'y': [2,4,5], 'type': 'bar', 'name':u'Montreal'}
            ],
            'layout': {
                'title':'Dash Data Visualisation'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)