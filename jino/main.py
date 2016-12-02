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
from flask import g
import logging
import sqlite3
import yaml

import jino.parser

logging.basicConfig(level=logging.INFO, format='%(message)s')
LOG = logging.getLogger(__name__)

DEFAULT_CONFIG = '/etc/jino/config.yaml'

app = Flask(__name__)

# Removing the following line will raise the
# following exception: 'Must provide secret_key to use csrf'.
app.secret_key = 'you_will_never_guess'


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_db():
    """Opens a new database connection if there is none yet for the

    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def read_config(conf):
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


def main():
    from jino.views import home

    parser = jino.parser.create()
    args = parser.parse_args()

    app.config['jobs'], app.config['titles'] = read_config(
        args.config or DEFAULT_CONFIG)

    for arg in vars(args):
        app.config[arg] = getattr(args, arg)

    app.config.from_object('jino.config')
    app.run()

if __name__ == '__main__':
    main()
