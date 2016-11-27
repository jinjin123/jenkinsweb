# Copyright 2016 Arie Bregman
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
import jenkins

import jino.jenkins as jenk
from jino.main import app


@app.route('/')
def home():

    # Create Jenkins server instance
    server = jenkins.Jenkins(app.config['jenkins'], app.config['username'],
                             app.config['password'])

    # todo(abregman): run only once a day, and keep nightly status in the DB
    jobs_status = jenk.get_jobs_status(server, app.config['jobs'])

    return render_template('home.html', jobs=app.config['jobs'],
                           status=jobs_status, titles=app.config['titles'])
