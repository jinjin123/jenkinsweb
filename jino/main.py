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
from flask import Flask
from flask_script import prompt_bool
from flask_sqlalchemy import SQLAlchemy
import logging
import sys
import yaml

import jino.jenkins_lib as jenkins
import jino.parser

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)

# Create the application
app = Flask(__name__)

# Load in-project config
app.config.from_object('jino.config')

# Initialize Jino database
db = SQLAlchemy(app)

# Removing the following line will raise the
# following exception: 'Must provide secret_key to use csrf'.
app.secret_key = 'you_will_never_guess'


def get_jobs(conf):
    """Reads configuration and returns dict of jobs and their attributes.

    Example:
        {'my_job':
            'title': 'a title for my awesome job'
            'table': 'table number 1'}
    """
    jobs = {}

    with open(conf, 'r') as f:
        conf = yaml.load(f)
        for table in conf:
            for job in table['jobs']:
                jobs[job['name']] = {}
                jobs[job['name']]['title'] = job['title']
                jobs[job['name']]['table'] = table

    return jobs


def create_db_tables():
    """Creates all the tables."""
    db.create_all()


def drop_db_tables():
    """Drops all the tables."""
    if prompt_bool("You are about to remove all the data!!! \
You sure you want to proceed?"):
        db.drop_all()


def parse_args():
    """Returns argparse arguments namespace."""
    parser = jino.parser.create()
    args = parser.parse_args()

    return args


def check_valid_args(args):
    """Checks there is a right combination of passed arguments."""
    if (not args.config and not args.jenkins):
        LOG.error("You must either provide config file with --conf \
or the arguments '--jenkins --username and --password'")
        sys.exit(2)


def set_configuration(args):
    """Set app configuration based on the given arguments."""

    if args.jenkins:
        for arg in vars(args):
            app.config[arg.upper()] = getattr(args, arg)
    else:
        app.config.from_pyfile(args.config)


def update_database(jobs, jenkins_c):
    """Makes sure the database contains information on each given job."""

    db_jobs = models.Job.query.all()

    if not db_jobs:
        LOG.info("Didn't find any entries in the database. Retrieving \
information from Jenkins...")

        for job, job_attr in jobs.iteritems():

            last_build_status = jenkins_c.get_last_build_status(job)
            LOG.info("Retrieved information for: %s", job)

            if last_build_status == 'SUCCESS':
                button_status = 'btn-success'
            else:
                button_status = 'btn-danger'

            db.session.add(models.Multi_Job(name=job, status=last_build_status,
                                            title=job_attr['title'],
                                            button_status=button_status))
            db.session.commit()
    else:
        LOG.info("Database already exists...skipping to running server.")


def create_jenkins_client():
    """Returns jenkins.Jenkins instance."""
    return jenkins.JenkinsClient(app.config['JENKINS'],
                                 app.config['USERNAME'],
                                 app.config['PASSWORD'])


def main():
    # Parse arguments
    args = parse_args()

    if args.parser == 'drop':
        drop_db_tables()

    elif args.parser == 'runserver':

        create_db_tables()
        check_valid_args(args)
        set_configuration(args)
        jenkins_c = create_jenkins_client()
        app.config['jobs'] = get_jobs(args.jobs)
        update_database(app.config['jobs'], jenkins_c)

        app.run()


if __name__ == '__main__':
    main()

import jino.models as models
from jino.views import home
