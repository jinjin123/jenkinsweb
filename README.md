# Jino

![TravisCI](https://travis-ci.org/bregman-arie/jino.svg)
https://travis-ci.org/bregman-arie/jino

NOTE: The project is in the middle of a refactor process. It's NOT USABLE at the moment.

Jino is a web server for managing single or multiple Jenkins instances.

It allows you to:

    * Display jobs from multiple Jenkins instances

* [Requirements](#requirements)
* [Installation](#installation)
* [Getting Started](#getting-started)
* [Configuration](#configuration)
* [Screenshots](#screenshots)

## Requirements

* Python >= 2.7

## Installation

    virtualenv .venv && source .venv/bin/activate
    pip install .

You can also run the quick setup script in this directory:

    chmod +x scripts/quick_run.sh && scripts/quick_run.sh

## Run Jino Web Application

    jino-server run

## Configuration 

The default location for Jino configuration is '/etc/jino/jino.conf'.
You can specify it by using the CLI: --conf <conf_file_path>

You can find sample in samples/jino.conf

Minimal configuration:

    [jenkins/instance1]

    url = https://<jenkins_instance_address>
    user = jenkins_user
    password = jenkins_user_password

## The technologies behind Jino

* Flask
* SQLite
* Patternfly

## Screenshots

<div align="center"><img src="./doc/jino_main_page.png" alt="Jino Main Page" width="800"></div><hr />
