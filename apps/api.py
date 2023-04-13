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
import os

from dash import html

import flask
from flask import Blueprint
from flask import request, jsonify, Response

import pandas as pd

#from myapp import add_numbers
def add_numbers(a, b):
    return a + b

api_bp = Blueprint('', __name__)

args_objects = [
    {
        'name': 'num1',
        'required': True,
        'description': 'First number (numeric)'
    },
    {
        'name': 'num2',
        'required': True,
        'description': 'Second number (numeric)'
    }
]

args_ci = [
    {
        'name': 'branch',
        'required': True,
        'description': 'branch name'
    }
]

@api_bp.route('/api/v1/add_numbers', methods=['GET'])
def return_object_arguments():
    """ Obtain information about the `add_numbers` microservice
    """
    if len(request.args) > 0:
        # POST from query URL
        return return_object(payload=request.args)
    else:
        return jsonify({'args': args_objects})

@api_bp.route('/api/v1/add_numbers', methods=['POST'])
def return_object(payload=None):
    """ Sum two numbers
    """
    # get payload from the JSON
    if payload is None:
        payload = request.json

    # Check all required args are here
    required_args = [i['name'] for i in args_objects if i['required'] is True]
    for required_arg in required_args:
        if required_arg not in payload:
            rep = {
                'status': 'error',
                'text': "A value for `{}` is required. Use GET to check arguments.\n".format(required_arg)
            }
            return Response(str(rep), 400)

    out = add_numbers(payload['num1'], payload['num2'])
    pdf = pd.DataFrame({'Result': [out]})

    return pdf.to_json(orient='records')

@api_bp.route('/api/v1/ci', methods=['POST'])
def trigger_ci(payload=None):
    """ Trigger the CI
    """
    # get payload from the JSON
    if payload is None:
        payload = request.json

    # Check all required args are here
    required_args = [i['name'] for i in args_ci if i['required'] is True]
    for required_arg in required_args:
        if required_arg not in payload:
            rep = {
                'status': 'error',
                'text': "A value for `{}` is required. Use GET to check arguments.\n".format(required_arg)
            }
            return Response(str(rep), 400)

    # Execute the CI

    rep = {
        'status': 'success',
        'text': "CI has started for branch {}.\n".format(payload['branch'])
    }
    return Response(str(rep), 200)
