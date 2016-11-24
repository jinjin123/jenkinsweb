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
import logging

LOG = logging.getLogger('__main__')


def get_jobs_status(server, jobs):
    """Returns dict of jobs and their status

    :param server: Jenkins server instance
    :param jobs: list of jobs
    """

    jobs_status = {}

    try:
        for job in jobs:
            last_build_num = server.get_job_info(
                job)['lastCompletedBuild']['number']
            status = str(server.get_build_info(
                job, last_build_num)['result'])

            jobs_status[job] = status

    except Exception:
        LOG.info("Could not get information for %s", job)

    return jobs_status
