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
* Configuration - Which jobs you are interested in

To run Jino::

    jino runserver --jenkins 'http://my_jenkins' --username X --password Y --config /etc/jino/config.ini

Configuration
-------------

Using YAML format::

    - name: neutron
		title1:
		  - job_name1
		title2:
		  - job_name2
		title3:
		  - job_name3
