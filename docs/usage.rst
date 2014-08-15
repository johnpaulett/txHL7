Usage
=====

Run simple demo server on default port 2575::

    twistd --nodaemon mllp

Run simple server with a custom receiver on port 7575::

    twistd --nodaemon mllp --endpoint tcp:7575 --receiver myreceiver.Receiver

Options help::

    twistd mllp --help

Installation of this package may result in a warning which can be ignored::

    package init file 'twisted/plugins/__init__.py' not found (or not a regular file)
