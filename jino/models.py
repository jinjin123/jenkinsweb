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
from jino.main import db


job_multi_job = db.Table('job_multi_job',
                         db.Column('job_name', db.String(64),
                                   db.ForeignKey('job.name')),
                         db.Column('multi_job_name', db.String(64),
                                   db.ForeignKey('multi_job.name')),
                         )


class Multi_Job(db.Model):
    """Represents Jenkins multi job."""

    __tablename__ = 'multi_job'

    name = db.Column(db.String(64), primary_key=True,
                     index=True, unique=True)

    status = db.Column(db.String(64))
    button_status = db.Column(db.String(64))

    title = db.Column(db.String(64))

    sub_jobs = db.relationship('Job', secondary=job_multi_job,
                               backref=db.backref('multi_jobs',
                                                  lazy='dynamic'))

    def __repr__(self):
        return "<Multi Job %r" % (self.name)


class Job(db.Model):
    """Represents Jenkins job."""

    __tablename__ = 'job'

    name = db.Column(db.String(64), primary_key=True,
                     index=True, unique=True)

    status = db.Column(db.String(64))
    button_status = db.Column(db.String(64))

    def __repr__(self):
        return "<Job %r" % (self.name)
