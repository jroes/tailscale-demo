import subprocess
import os
from enum import Enum

class ConnectionState(Enum):
    CONNECTED = 1
    NOT_CONNECTED = 2
    CONNECTING = 3
    FAILED = 4

class SSHTunnel:
    def __init__(self, ssh_private_key, ssh_user, ssh_host):
        self.proc = None
        self.state = ConnectionState.NOT_CONNECTED
        self.ssh_private_key = ssh_private_key
        self.ssh_user = ssh_user
        self.ssh_host = ssh_host

    def connect(self):
        os.system(f"mkdir -p ~/.ssh && chmod 700 ~/.ssh")
        with open("/home/appuser/.ssh/key", "w") as f:
            f.write(self.ssh_private_key)
        os.chmod("/home/appuser/.ssh/key", 0o600)  # user read/write only
        os.system(
            f"mkdir -p ~/.ssh && ssh-keyscan -H {self.ssh_host} >> ~/.ssh/known_hosts"
        )
        self.state = ConnectionState.CONNECTING
        self.proc = subprocess.Popen(
            [
                "ssh",
                "-i",
                "~/.ssh/key",
                "-4",
                "-fNT",
                "-L",
                f"54321:localhost:5432",
                f"{self.ssh_user}@{self.ssh_host}",
            ]
        )
        # os.remove("~/.ssh/key") # no need to keep on disk

    def disconnect(self):
        self.proc.kill()
        self.proc = None
        self.state = ConnectionState.NOT_CONNECTED

    def is_connected(self):
        return self.state == ConnectionState.CONNECTED

    def is_connecting(self):
        return self.state == ConnectionState.CONNECTING

    def is_not_connected(self):
        return self.state == ConnectionState.NOT_CONNECTED

    def is_failed(self):
        return self.state == ConnectionState.FAILED

    def evaluate_state(self):
        if self.proc is not None:
            self.proc.poll()
            if self.proc.returncode == 0:
                self.state = ConnectionState.CONNECTED
            else:
                self.state = ConnectionState.FAILED
        else:
            self.state = ConnectionState.NOT_CONNECTED

    def get_output(self):
        return self.proc.returncode
        #return [self.proc.stdout.read(), self.proc.stderr.read()]
