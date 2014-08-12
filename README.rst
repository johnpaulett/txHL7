
Setup environment::

    virtualenv --no-site-packages env
    source env/bin/activate
    pip install -r dev_requirements.txt

Run tests::

    trial tests

Run simple demo server on default port 2575::

    twistd --nodaemon mllp

Run simple server with a custom receiver on port 7575::

    twistd --nodaemon mllp --endpoint tcp:7575 --receiver myreceiver.Receiver

Options help::

    twistd mllp --help
