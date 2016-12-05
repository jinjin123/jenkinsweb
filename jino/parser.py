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
import argparse


def create():
    """Returns argparse parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument('runserver', help='Run Jino')
    parser.add_argument('--jenkins', '-j', dest="jenkins", help='Jenkins URL')
    parser.add_argument('--username', '-u', dest="username", help='Jenkins username')
    parser.add_argument('--password', '-p', dest="password", help='Jenkins user password')
    parser.add_argument('--conf', '-c', dest="config", help='Jino configuration')
    parser.add_argument('--jobs', dest="jobs",
                        help='Jenkins Jobs YAML', required=True)

    return parser
