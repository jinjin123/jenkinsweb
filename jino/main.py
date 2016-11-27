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
import yaml

import jino.parser

DEFAULT_CONFIG = '/etc/jino/config.yaml'

app = Flask(__name__)


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
