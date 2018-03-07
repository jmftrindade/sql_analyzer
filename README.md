Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Structure](#structure)
   * [Dependencies](#dependencies)
      * [node-js](#node.js)
      * [python](#python)

# SQL Analyzer

A small end-to-end example on how to automagically extract stats from a list of input -- well-formed ;P -- SQL queries. Take a look at [`analyzer.py`](src/analyzer/analyzer.py) for example stats, which currently includes number of joins, list of referenced tables, number of group by columns, etc.

To add your own stats, you'll need to understand [JMESPath](http://jmespath.org), which is kinda like XPath, but for JSON.  It's pretty easy to grasp, and their [examples page](http://jmespath.org/examples.html) is a great place to start.

After you learn the basics -- shouldn't take you more than 5 minutes if you're already familiar with XPath -- just modify the included [`analyzer.py`](src/analyzer/analyzer.py).

Aside from examples on how to get *structural* stats from SQL queries, I also included in the analyzer a toy example on how to use an LSH forest index for top-k query similarity.  You can use it to e.g., find candidate queries that are textually similar to a given problematic query.

# Structure

- [`data/`](data/): Example input and output data.  Current list of example queries shamelessly stolen from Raul's [nqo](http://github.com/raulcf/nqo/tree/master/raw_query_data) project.
- [`src/`](src/): Source code for SQL parser and analyzer with example usage.

# Dependencies

## node.js

nodejs (for sqlite parser):
```
$ curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
$ sudo apt-get install -y nodejs npm build-essential
$ sudo ln -s /usr/bin/nodejs /usr/bin/node

# node deps (run from this directory):
$ npm install
```

## python

analyzer:
```
$ sudo apt-get install python-setuptools
$ pip install -r requirements.txt
```
