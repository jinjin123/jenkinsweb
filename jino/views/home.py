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
from flask import request
from flask import jsonify
from flask_wtf import Form
import jenkins
import logging
from wtforms import SubmitField

import jino.jenkins as jenk
from jino.main import app

LOG = logging.getLogger('__main__')


class Result(Form):
        job_result = SubmitField()


@app.route('/')
def home():
    form = Result()

    # Create Jenkins server instance
    server = jenkins.Jenkins(app.config['jenkins'], app.config['username'],
                             app.config['password'])

    # todo(abregman): run only once a day, and keep nightly status in the DB
    jobs_status = jenk.get_jobs_status(server, app.config['jobs'])

    LOG.info("Jobs data: %s", jobs_status)

    return render_template('home.html', jobs=app.config['jobs'],
                           status=jobs_status, titles=app.config['titles'],
                           form=form)


@app.route('/result/<job>', methods=['GET','POST'])
def result(job):
    x=2

@app.route('/_get_job_detailed_result')
def get_job_detailed_result():
    
    # Create Jenkins server instance
    server = jenkins.Jenkins(app.config['jenkins'], app.config['username'],
                             app.config['password'])

    detailed_result = jenk.get_job_detailed_result(server,
        'neutron-nightly-rhos-5.0-coreci')

    return jsonify(result=detailed_result)
    #a = request.args.get('a', 0, type=int)
    #b = request.args.get('b', 0, type=int)
    #return jsonify(result=a + b)
