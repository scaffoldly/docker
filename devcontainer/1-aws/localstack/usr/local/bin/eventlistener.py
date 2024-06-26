#!/usr/bin/env python
from time import sleep
from supervisor.childutils import listener
import subprocess
import sys
import os
import json

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

public_ports_path = '/etc/scaffoldly/public-ports'
public_ports = []
if os.path.exists(public_ports_path):
    with open(public_ports_path, 'r') as file:
        public_ports = [port.strip() for port in file.readline().strip().split(',')]


def get_secret(key_name):
    env_secrets = '/workspaces/.codespaces/shared/.env-secrets'

    if os.path.exists(env_secrets):
        with open(env_secrets, 'r') as file:
            for line in file:
                if line.startswith(f"{key_name}="):
                    # Split the line at '=' and strip any whitespace or newlines
                    _, encoded_value = line.strip().split('=', 1)
                    return decode_base64(encoded_value)

    # Fallback to env, default None
    return os.environ.get(key_name, None)


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


def wait_for_port(port, max_attempts = 60):
    if max_attempts <= 0:
        return False

    if not port:
        return False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', int(port)))
        sock.close()

        if result != 0:
            raise Exception("Port is not open")

    except Exception as e:
        sleep(1)
        return wait_for_port(port, max_attempts-1)

    return True


def wait_then_start(port, thenstart):
    wait_for_port(port)
    start(thenstart)


def wait_then_stop(port, thenstop):
    wait_for_port(port)
    stop(thenstop)


def open_port(port, max_attempts = 60):
    if max_attempts <= 0:
        return False

    if not port:
        return False

    codespace_name = get_secret("CODESPACE_NAME")
    if not codespace_name:
        return False

    github_token = get_secret("GITHUB_TOKEN")
    if not github_token:
        return False

    try:
        # TODO Switch to API calls
        result = subprocess.run(["gh", "codespace", "ports", "-c", codespace_name, "--json", "sourcePort,visibility"], env={'GH_TOKEN':github_token}, check=True, text=True, capture_output=True)
        json_data = json.loads(result.stdout)
        item = next((item for item in json_data if item['sourcePort'] == int(port)), None)
        if not item:
            raise Exception("Port not found")
        if item.get("visibility") == "public":
            return False
    except Exception as e:
        sleep(1)
        return open_port(port, max_attempts-1)

    write_stderr(f"Opening port {port} for {codespace_name}")
    # TODO Switch to API calls
    output = subprocess.run(["gh", "codespace", "ports", "visibility", "-c", codespace_name, f"{port}:public"], env={'GH_TOKEN':github_token})

    return True


def set_aws_config(port):
    if not port:
        os.system(f"aws configure set default.endpoint_url \"\"")
        return

    endpoint_url = f"http://localhost.localstack.cloud:{port}"

    codespace_name = get_secret("CODESPACE_NAME")
    domain = get_secret("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")

    if codespace_name and domain:
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


def ensure_public_ports(exclude=[]):
    for port in public_ports:
        if port in exclude:
            break

        if not wait_for_port(port, 1):
            break
        
        if not open_port(port, 1):
            break
        
        public_ports.remove(port)


def main():
    localstack_port = os.getenv("LOCALSTACK_PORT", None)
    localstack_running = False

    while True:
        headers, body = listener.wait(sys.stdin, sys.stdout)
        body = dict([pair.split(":") for pair in body.split(" ")])

        eventname = headers["eventname"]
        processname = body["processname"] if "processname" in body else "supervisor"

        write_stderr(f"Received {eventname} from {processname}.")

        if eventname == "TICK_5":
            ensure_public_ports(exclude=[localstack_port])

            if localstack_running:
                # HACK: Startup ordering:
                #       - it appears that the port flips back to private sometime in the startup process
                open_port(localstack_port)

        if eventname == "PROCESS_STATE_STARTING":
            if processname == "localstack":
                set_aws_config(localstack_port)

        if eventname == "PROCESS_STATE_RUNNING":
            if processname == "localstack":
                wait_for_port(localstack_port)
                open_port(localstack_port)
                load_localstack_pod()
                localstack_running = True

        if eventname == "PROCESS_STATE_STOPPING":
            if processname == "localstack":
                localstack_running = False
                save_localstack_pod()

        if eventname == "PROCESS_STATE_STOPPED":
            if processname == "localstack":
                set_aws_config(None)

        # acknowledge the event
        write_stdout("RESULT 2\nOK")


if __name__ == '__main__':
    main()
