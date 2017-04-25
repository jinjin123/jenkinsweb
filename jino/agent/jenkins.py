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
import time

from jino.agent import agent


class JenkinsAgent(agent.Agent):

    def __init__(self, name, user, password, url):
        super(JenkinsAgent, self).__init__(name)

        self.user = user
        self.password = password
        self.url = url

    def start(self):
        """Start running the jenkins agent."""
        while True:
            print("Pulled data")
            time.sleep(5)
