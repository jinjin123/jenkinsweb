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
from flask import Flask
from gevent.pywsgi import WSGIServer
import logging

import jino.parser
from jino.web import webapp

logger = logging.getLogger(__name__)


class Manager(object):
    """Manages Jino run.

    Creates configuration based on passed arguments.
    """
    DEFAULT_BIND_HOST = '0.0.0.0'
    DEFAULT_PORT = 5000

    def __init__(self):

        config = self._load_config()
        self.app = self._create_app(config)
        self.app.register_blueprint(webapp)
        self._setup_logging()

    def _create_app(self, config):
        """Returns Flask application."""
        app = Flask(__name__)
        app.config.update(config)

        return app

    def _load_config(self):
        """Load arguments as passed by the user.

        returns dictionary of configartion options and their value.
        """
        config = {}

        parser = jino.parser.create()
        args = parser.parse_args()

        # Convert Namespace instance into a dictionary of args:values
        # so we can load them into Flask configuration
        for k, v in vars(args).iteritems():
            key = 'JINO_{}'.format(k.upper())
            config[key] = v

        return config

    def _setup_logging(self):
        """Setup logging level."""
        format = '%(levelname)s: %(name)s | %(message)s'
        level = self.app.config.get('JINO_LOG_LEVEL', logging.INFO)
        logging.basicConfig(level=level, format=format)
        logging.getLogger(__name__)

    def _run_web(self):
        """Runs the web server."""
        logger.info("Running Jino web server")

        log = 'default' if self.app.debug else None
        listen_socket = (
            self.app.config.get('JINO_BIND_HOST', self.DEFAULT_BIND_HOST),
            self.app.config.get('JINO_PORT', self.DEFAULT_PORT)
        )

        self.server = WSGIServer(listen_socket,
                                 application=self.app,
                                 log=log)
        self.server.serve_forever()

    def _run_agent(self):
        """Runs Jino agent."""
        pass

    def run(self):
        """Runs Jino in server or agent mode."""
        if self.app.config.get("JINO_AGENT"):
            return self._run_agent()
        else:
            return self._run_web()


def main():

    manager = Manager()
    manager.run()


if __name__ == '__main__':
    main()
