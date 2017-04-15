# Jino

NOTE: The project is in the middle of a refactor process. It's NOT USABLE at the moment.

Jino is a web server for managing single or multiple Jenkins instances.

It allows you to:

    * Display jobs from multiple Jenkins instances
    

* [Installation](#installation)
* [Configuration](#configuration)
* [Screenshots](#screenshots)

## Installation

The short way:

    chmod +x quick_setup.sh && ./quick_setup.sh

The "long" way:

    virtualenv .venv && source .venv/bin/activate
    pip install .

To run Jino:

    jino runserver --conf /etc/jino/jino.conf --jobs /etc/jobs.yaml

Configuration
-------------

Jino uses the configuration mechanism offered by Flask.

In addition to the [built-in configuration offered by Flask](http://flask.pocoo.org/docs/config/#builtin-configuration-values) there's a number of jino specific ones as well:

| Name | Description |
| ---- | ----------- |
| `JINO_LOG_LEVEL` | The log level (INFO, DEBUG). | 

## Screenshots

<div align="center"><img src="./doc/jino_main_page.png" alt="Jino Main Page" width="800"></div><hr />
