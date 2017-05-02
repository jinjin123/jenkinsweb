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
import jenkins
import logging
from multiprocessing import Process
import time

from jino.agent import agent
import jino.lib.jenkins as jenkins_lib
import jino.models.job as job_model
import jino.models.agent as agent_model
from jino.db.base import db

LOG = logging.getLogger(__name__)


class JenkinsAgent(agent.Agent):

    def __init__(self, name, user, password, url, app):

        super(JenkinsAgent, self).__init__(name)
        self.user = user
        self.password = password
        self.url = url
        self.app = app
        self.pre_run_process = Process(target=self.pre_start)
        if user and password:
            self.conn = jenkins.Jenkins(self.url, self.user, self.password)
        else:
            self.conn = jenkins.Jenkins(self.url)
        self.add_agent_to_db()

    def start(self):
        """Start running the jenkins agent."""
        while True:
            time.sleep(10)
            db.session.remove()

    def pre_start(self):
        """Populate the database with all the information from Jenkins."""
        with self.app.app_context():

            # Initial update. Adds all the jobs with only their name to the DB
            all_jobs = self.conn.get_all_jobs()
            for job in all_jobs:
                db_job = job_model.Job(name=job['name'],
                                       jenkins_server=self.name)
                db.session.add(db_job)
                db.session.commit()
                LOG.debug("Added job from %s: %s to \
the database" % (self.name, job['name']))

            for job in all_jobs:
                # Now pull specific information for each job
                job_info = self.conn.get_job_info(job['name'])
                last_build_number = jenkins_lib.get_last_build_number(job_info)
                if last_build_number:
                    last_build_result = jenkins_lib.get_build_result(
                        self.conn, job['name'], last_build_number)
                else:
                    last_build_result = "None"

                # Update entry in database
                db_job = job_model.Job.query.filter_by(
                    name=job['name']).update(
                        dict(last_build_number=last_build_number,
                             last_build_result=last_build_result))
                db.session.commit()
                LOG.debug("Updated job from %s: %s" % (self.name, job['name']))

    def add_agent_to_db(self):
        """Adds the agent to the database."""
        with self.app.app_context():
            db_agent = agent_model.Agent(name=self.name)
            db.session.add(db_agent)
            db.session.commit()
