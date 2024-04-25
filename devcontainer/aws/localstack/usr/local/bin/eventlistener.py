#!/usr/bin/env python
from time import sleep
from supervisor.childutils import listener
import subprocess
import sys
import os

from xmlrpc.client import ServerProxy

import socket
import base64


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(f"{s}\n")
    sys.stderr.flush()


def decode_base64(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    decoded_bytes = base64.b64decode(data)
    return decoded_bytes.decode('utf-8')


class SupervisorClient(object):
    def __init__(self, host='127.0.0.1', port=9999):
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


def get_secret(key_name, max_attempts = 60):
    env_secrets = '/workspaces/.codespaces/shared/.env-secrets'

    if max_attempts < 0:
        write_stderr(f"Gave up looking for '{key_name}' from '{env_secrets}'!")
        return None

    if not os.path.exists(env_secrets):
        write_stderr(f"Waiting for '{env_secrets}' to exist...")
        sleep(1)
        return get_secret(key_name, max_attempts - 1)

    with open(env_secrets, 'r') as file:
        for line in file:
            if line.startswith(f"{key_name}="):
                # Split the line at '=' and strip any whitespace or newlines
                _, encoded_value = line.strip().split('=', 1)
                return decode_base64(encoded_value)

    return None


def start(process):
    try:
        supervisor.start(process)
    except Exception as e:
        write_stderr(f"WARN: Unable to start: {e}")

def stop(process):
    try:
        supervisor.stop(process)
    except Exception as e:
        write_stderr(f"WARN: Unable to stop: {e}")


def wait_for_port(port):
    write_stderr(f"Waiting for port {port}...")
    sleep(1)

    if not port:
        return

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', int(port)))
        sock.close()

        if result == 0:
            return
        else:
            wait_for_port(port)

    except Exception as e:
        wait_for_port(port)

def wait_then_start(port, thenstart):
    wait_for_port(port)
    start(thenstart)

def wait_then_stop(port, thenstop):
    wait_for_port(port)
    stop(thenstop)


def open_port(port):
    if not port:
        return

    codespace_name = get_secret("CODESPACE_NAME")
    if not codespace_name:
        return

    github_token = get_secret("GITHUB_TOKEN")
    if not github_token:
        return

    write_stderr(f"Opening port {port} for {codespace_name}")
    os.environ["GH_TOKEN"] = github_token
    output = subprocess.run(["gh", "codespace", "ports", "visibility", "-c", codespace_name, f"{port}:public"], shell=True, capture_output=True, text=True)
    write_stderr(output)


def set_aws_config(port):
    if not port:
        os.system(f"aws configure set default.endpoint_url \"\"")
        return

    codespace_name = get_secret("CODESPACE_NAME")
    if not codespace_name:
        return

    domain = get_secret("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    if not domain:
        return

    endpoint_url = f"https://{codespace_name}-{port}.{domain}"
    write_stderr(f"Setting default AWS endpoint to for {endpoint_url}")
    os.system(f"aws configure set default.endpoint_url {endpoint_url}")


def load_localstack_pod():
    pod_path = os.getenv("POD_PATH")

    if not pod_path or not os.path.exists(pod_path):
        return
    
    write_stderr("NOT IMPLEMENTED: Restoring localstack state")

def save_localstack_pod():
    pod_path = os.getenv("POD_PATH")

    if not pod_path or not os.path.exists(pod_path):
        return

    write_stderr("NOT IMPLEMENTED: Saving localstack state")

def main():
    localstack_port = os.getenv("LOCALSTACK_PORT", None)

    while True:
        headers, body = listener.wait(sys.stdin, sys.stdout)
        body = dict([pair.split(":") for pair in body.split(" ")])

        eventname = headers["eventname"]
        processname = body["processname"]

        write_stderr(f"Received {eventname} from {processname}.")

        if eventname == "PROCESS_STATE_STARTING":
            if processname == "localstack":
                set_aws_config(localstack_port)

        if eventname == "PROCESS_STATE_RUNNING":
            if processname == "localstack":
                wait_for_port(localstack_port)
                open_port(localstack_port)
                load_localstack_pod()

        if eventname == "PROCESS_STATE_STOPPING":
            if processname == "localstack":
                save_localstack_pod()

        if eventname == "PROCESS_STATE_STOPPED":
            if processname == "localstack":
                set_aws_config(None)

        # acknowledge the event
        write_stdout("RESULT 2\nOK")


if __name__ == '__main__':
    main()
