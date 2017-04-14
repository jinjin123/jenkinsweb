Jino
====

NOTE: The project is in the middle of a refactor process. It's NOT USABLE at the moment.

Jino is a web server for managing single or multiple Jenkins instances.

It allows you to:

    * Display jobs from multiple Jenkins instances

<div align="center"><img src="./doc/jino_main_page.png" alt="Jino Main Page" width="800"></div><hr />

Installation
------------

The short way:

    chmod +x quick_setup.sh && ./quick_setup.sh

The "long" way:

    virtualenv .venv && source .venv/bin/activate
    pip install .

Running the server
------------------

To run Jino:

    jino runserver --conf /etc/jino/jino.conf --jobs /etc/jobs.yaml


Configuration
-------------

You must specify at least one server in the config file:

[server/jenkins1]

server = http://<jenkins_server>
username = <Jenkins user>
password = <Jenkins user password>

The location of the config file specified by --conf. By default, Jino will look for /etc/jino/jino.conf


Jobs
----

Using YAML format:

    - table: neutron
      jobs:
		- title: "Title of the first row"
		  name: "jenkins-job-name1"

		- title: "Title of the second row"
		  name: "jenkins-job-name2"

The location specified by --jobs. By default, Jino will look for /etc/jino/jobs.yaml.


Drop database tables
--------------------

To drop all the tables, run:

    jino drop
