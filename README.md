Jino
====

Jino is a dashboard, used for managing and monitoring Jenkins.

Installation
------------

To install jino, run the following command:

    sudo pip install jino

Usage
-----

Jino requires several arguments in order to run properly:

* Jenkins URL   - the url of your Jenkins server (e.g http://my_jenkins)
* Username      - Jenkins username
* Password      - Jenkins password
* Configuration - Jino will build the home page tables based on the configuration

To run Jino::

    jino runserver --jenkins 'http://my_jenkins' --username X --password Y --config /etc/my_jino_config.yaml

Configuration
-------------

Using YAML format::

    - table: neutron
      jobs:
		- title: "Title of the first row"
		  name: "jenkins-job-name1"

		- title: "Title of the second row"
		  name: "jenkins-job-name2"

The location specified by --config. By default, Jino will look for /etc/jino/config.yaml.
