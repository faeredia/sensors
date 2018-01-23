#use anaconda to run app
#anaconda-on

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html

from conn import db_conn

#Fetch data from the server
#keep the connection details somewhere safe on the server side.
df = pd.read_sql('SELECT * FROM generic_sensor_data', db_conn)
db_conn.close()

app = add.Dash()

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