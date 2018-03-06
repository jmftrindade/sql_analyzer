Table of Contents
=================

   * [Table of Contents](#table-of-contents)
   * [Structure](#structure)
   * [Dependencies](#dependencies)
      * [node-js](#node.js)
      * [python](#python)

# Structure

- [`data/`](data/): Example input and output data.
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
