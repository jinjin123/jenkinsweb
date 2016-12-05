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


def read_jobs(conf):
    """Reads config."""
    jobs = []
    titles = []

    with open(conf, 'r') as f:
        conf = yaml.load(f)
        for table in conf:
            for job in table['jobs']:
                jobs.append(job['name'])
                titles.append(job['title'])

    return jobs, titles


def add_job_to_db(job):
    """Adds Jenkins job to the database."""

    db.session.add(job)
    db.session.commit()


def create_db_tables():
    """Creates all the tables."""
    db.create_all()


def drop_db_tables():
    """Drops all the tables."""
    if prompt_bool("You are about to remove all the data!!! \
                   You sure you want to proceed?"):
        db.drop_all()


def main():
    from jino.views import home

    # Initalize database
    db.create_all()

    parser = jino.parser.create()
    args = parser.parse_args()
    if (not args.config and not args.jenkins):
        LOG.error("You must either provide config file with --conf \
or the arguments '--jenkins --username and --password'")
        sys.exit(2)

    app.config['jobs'], app.config['titles'] = read_jobs(
        args.jobs)

    # Load Jenkins URL, username and password values
    if args.jenkins:
        for arg in vars(args):
            app.config[arg] = getattr(args, arg)
    else:
        app.config.from_pyfile(args.config)

    app.run()

if __name__ == '__main__':
    main()
