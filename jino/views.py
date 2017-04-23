# Copyright 2017 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
import logging


logger = logging.getLogger(__name__)

webapp = Blueprint('jino', __name__, static_folder='static')


@webapp.route('/')
def home():
    """Home page."""
    return render_template('home.html')


@webapp.route('/agents')
def agents():
    """Agents page"""
    return render_template('agent.html')


@webapp.route('/register')
def register_jenkins():
    name = request.args['name']
    port = request.args['port']
    host = request.remote_addr

    current_app.jino.register_jenkins(name, host, port)
    return jsonify({'status': 'OK'})
