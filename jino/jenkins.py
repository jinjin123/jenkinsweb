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
import sys

LOG = logging.getLogger('__main__')


def get_jobs_status(server, jobs):
    """Returns dict of jobs and their status

    :param server: Jenkins server instance
    :param jobs: list of jobs
    """

    jobs_status = {}

    try:
        for job in jobs:
            jobs_status[job] = {}
            last_build_num = server.get_job_info(
                job)['lastCompletedBuild']['number']
            status = str(server.get_build_info(
                job, last_build_num)['result'])
            sub_jobs = server.get_build_info(
                job, last_build_num)['subBuilds']

            if status == 'SUCCESS':
                jobs_status[job]['status'] = 'success'
                jobs_status[job]['button'] = 'btn-success'
            else:
                jobs_status[job]['status'] = 'failure'
                jobs_status[job]['button'] = 'btn-danger'

            jobs_status[job]['sub_jobs'] = {}

            for sub_job_dict in sub_jobs:
                sub_job = sub_job_dict['jobName']
                jobs_status[job]['sub_jobs'][sub_job] = {}
                sub_last_build_num = server.get_job_info(
                    sub_job)['lastCompletedBuild']['number']
                sub_status = str(server.get_build_info(
                    sub_job, sub_last_build_num)['result'])

                if status == 'SUCCESS':
                    jobs_status[job]['sub_jobs'][sub_job]['status'] = 'success'
                    jobs_status[job]['sub_jobs'][sub_job]['button'] = 'btn-success'
                else:
                    jobs_status[job]['sub_jobs'][sub_job]['status'] = 'failure'
                    jobs_status[job]['sub_jobs'][sub_job]['button'] = 'btn-danger'
                    
            #jobs_status[job]['subBuilds'] = [str(sub_job['jobName']) for sub_job in sub_jobs]
            LOG.info("Got info for job: %s", job)

    except Exception as e:
        LOG.info("Could not get information for %s", job['jobName'])
        LOG.info("Error: %s", e)
        sys.exit(2)

    return jobs_status


def get_job_detailed_result(server, job):
    """Return detailed job result."""

    last_build_num = server.get_job_info(
        job)['lastCompletedBuild']['number']

    output = server.get_build_console_output(job, last_build_num)

    #failure_url = server_url + '/job/' + job + '/' + str(last_build_num) + '/api/xml?depth=2}'
    #request = Request(failure_url)
    #auth = '%s:%s' % (username, password)
    #request.add_header('Authorization', auth)
    #failure = urlopen(request).read()

