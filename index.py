# Copyright 2023 Julien Peloton
# Author: Julien Peloton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import os
import logging

try:
    IP = os.environ['SSH_CONNECTION'].split(' ')[-2]
except KeyError:
    logging.warning("No SSH_CONNECTION found -- default is localhost")
    IP = "127.0.0.0"

PORT = 24000
APIURL = "http://{}:{}".format(IP, PORT)

# bootstrap theme
external_stylesheets = [
    dbc.themes.SPACELAB,
    '//use.fontawesome.com/releases/v5.7.2/css/all.css',
]
external_scripts = [
    '//code.jquery.com/jquery-1.12.1.min.js',
    '//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML',
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    meta_tags=[{
        "name": "viewport",
        "content": "width=device-width, initial-scale=1"
    }]
)

app.title = 'Coucou'

app.server.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
server = app.server

app.config.suppress_callback_exceptions = True

layout = html.Div(
    [
        html.Br(),
        html.Br(),
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        html.Img(
                            src="/assets/ijclab_logo.png",
                            height='100%',
                            width='30%'
                        )
                    ), style={'textAlign': 'center'}
                ),
                html.Br(),
                html.Br(),
                html.Br(),
            ], id='main_page', fluid=True
        ),
    ],
    className='home',
    style={'background-image': 'linear-gradient(rgba(255,255,255,0.3), rgba(255,255,255,0.3))', 'background-size': 'cover'}
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    layout
])

# register the API
try:
    from apps.api import api_bp
    server.register_blueprint(api_bp, url_prefix='/')
    server.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    server.config['JSON_SORT_KEYS'] = False
except ImportError as e:
    print('API not yet registered')

if __name__ == '__main__':
    app.run_server(IP, debug=True, port=PORT)
