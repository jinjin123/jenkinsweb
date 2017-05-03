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
from flask import render_template
from flask import Blueprint
import logging

import jino.models.job as job_model
import jino.models.agent as agent_model


logger = logging.getLogger(__name__)

home = Blueprint('home', __name__)


@home.route('/')
def index():
    """Home page."""
    jobs = job_model.Job.query
    agents = agent_model.Agent.query.all()
    return render_template('home.html', jobs=jobs, agents=agents)
