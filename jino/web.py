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
from configparser import ConfigParser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gevent.pywsgi import WSGIServer
import logging
import os

from jino.views import webapp
from jino.agent.jenkins import JenkinsAgent
import jino.db.create as jino_db
logger = logging.getLogger(__name__)


class WebApp(object):
    """Jino Web Application."""

    DEFAULT_BIND_HOST = '0.0.0.0'
    DEFAULT_PORT = 5000
    DEFAULT_CONFIG_FILE = '/etc/jino/jino.conf'

    def __init__(self, args_ns):

        self.agents = []

        self._setup_logging()
        self._setup_config(args_ns)
        if self.config['DEBUG']:
            self._update_logging_level(logging.DEBUG)
        self.app = self.create_app(self.config)
        self._setup_database()

    def _setup_config(self, args_ns):
        """Load configuration from different sources."""
        self.config = self._load_config_from_cli(args_ns)
        config_f = vars(args_ns)['config_file'] or self.DEFAULT_CONFIG_FILE
        if os.path.exists(config_f):
            self._load_config_from_file(config_f)

    def _setup_database(self):
        """Set up the database.

        Creates all the tables.
        """
        self.db = SQLAlchemy(self.app)
        jino_db.create_db(self.db, self.app.config)

    def create_app(self, config):
        """Returns Flask application."""
        app = Flask(__name__)
        app.register_blueprint(webapp)
        app.config.update(config)
        app.config.from_object('jino.db.config')

        return app

    def _load_config_from_cli(self, args_ns):
        """Load arguments as passed by the user.

        returns dictionary of configartion options and their values.
        """
        config = {}
        config['JENKINS_SERVERS'] = {}

        # Convert Namespace instance into a dictionary of args:values
        # so we can load them into Flask configuration
        for k, v in vars(args_ns).iteritems():
            config[k.upper()] = v

        return config

    def _load_config_from_file(self, config_f):
        """Loads configuration from file."""
        parser = ConfigParser()
        parser.read(config_f)

        for section in parser.sections():
            if section.startswith('jenkins/'):
                jenkins_name = section.split("/")[1]
                self.config['JENKINS_SERVERS'][jenkins_name] = {}
                for option in parser.options(section):
                    self.config['JENKINS_SERVERS'][jenkins_name][option] = \
                        parser.get(section, option)
            else:
                for option in parser.options(section):
                    self.config[option] = parser.get(section, option)
        logger.info("Updated config from file: %s" % config_f)
        logger.info("Configuration: %s" % self.config)

    def _setup_logging(self):
        """Setup logging level."""
        format = '%(levelname)s: %(name)s | %(message)s'
        level = logging.INFO
        logging.basicConfig(level=level, format=format)
        logging.getLogger(__name__)

    def _update_logging_level(self, logging_level):
        """Update logging based on passed level."""
        logging.getLogger().setLevel(logging.DEBUG)

    def setup_agents(self):
        """Create agents and start running them."""
        for instance_name, instance_conf in \
                self.app.config.get('JENKINS_SERVERS').iteritems():
            agent = JenkinsAgent(name=instance_name,
                                 user=instance_conf.get('user', None),
                                 password=instance_conf.get('password', None),
                                 url=instance_conf.get('url', None))
            self.agents.append(agent)
            logger.debug("Added new agent: %s" % instance_name)
            agent.process.start()

    def run(self):
        """Runs the web server."""
        logger.info("Running Jino web server")

        listen_socket = (
            self.app.config.get('BIND_HOST', self.DEFAULT_BIND_HOST),
            self.app.config.get('PORT', self.DEFAULT_PORT)
        )

        self.server = WSGIServer(listen_socket,
                                 application=self.app,
                                 log='default')
        self.server.serve_forever()
