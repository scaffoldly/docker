#!/usr/bin/env python
from time import sleep
from supervisor.childutils import listener
import sys

from xmlrpc.client import ServerProxy

import socket


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(f"{s}\n")
    sys.stderr.flush()


class SupervisorClient(object):
    """ Supervisor client to work with remote supervisor
    """

    def __init__(self, host='127.0.0.1', port=9001):
        self.server = ServerProxy('http://{}:{}/RPC2'.format(host, port))

    def _generate_correct_process_name(self, process):
        return "{}".format(process)

    def start(self, process):
        """ Start process
        :process: process name as String
        """
        return self.server.supervisor.startProcess(self._generate_correct_process_name(process))

    def stop(self, process):
        """ Stop process
        :process: process name as String
        """
        return self.server.supervisor.stopProcess(self._generate_correct_process_name(process))

    def status(self, process):
        """ Retrieve status process
        :process: process name as String
        """
        return self.server.supervisor.getProcessInfo(self._generate_correct_process_name(process))['statename']


supervisor = SupervisorClient()


def start(process):
    try:
        supervisor.start(process)
    except Exception as e:
        write_stderr(f"WARN: Unable to start: {e}")


def wait_then_start(port, thenstart):
    write_stderr(f"Waiting for port {port}...")
    sleep(1)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()

        if result == 0:
            start(thenstart)
        else:
            wait_then_start(port, thenstart)

    except Exception as e:
        wait_then_start(port, thenstart)


def main():

    while True:
        headers, body = listener.wait(sys.stdin, sys.stdout)
        body = dict([pair.split(":") for pair in body.split(" ")])

        eventname = headers["eventname"]
        processname = body["processname"]

        write_stderr(f"Received {eventname} from {processname}.")

        if eventname == "PROCESS_STATE_RUNNING":
            if processname == "health":
                wait_then_start(9000, "localstack")
            if processname == "localstack":
                wait_then_start(4566, "proxy")

        # acknowledge the event
        write_stdout("RESULT 2\nOK")

        if eventname == "PROCESS_STATE_RUNNING" and processname == "proxy":
            write_stderr(f"All services started!")
            supervisor.stop("startup")


if __name__ == '__main__':
    main()
