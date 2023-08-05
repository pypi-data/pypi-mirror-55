import typing
import argparse
import threading
import json
import socket
import contextlib
import time
import agutil.io

class SetupManager(object):
    """
    Manages setup/teardown for Canine jobs.
    Runs a small socketserver to provide setup and teardown data.
    """
    def __init__(self):
        """
        Initializes the Manager
        """
        self.setup = {}
        self.teardown = {}

    def add_job(self, jobId: str, setup: str, teardown: str):
        """
        Adds the given setup and teardown data for the job
        """
        self.setup[jobId] = setup
        self.teardown[jobId] = teardown

    def export(self, filepath_or_handle: typing.Union[str, typing.TextIO]):
        """
        Dumps the SetupManager to a json file, in a format meant for import on
        remote system
        """
        with contextlib.ExitStack() as stack:
            if isinstance(filepath_or_handle, str):
                filepath_or_handle = stack.enter_context(open(filepath_or_handle, 'w'))
            json.dump({
                'setup': self.setup,
                'teardown': self.teardown
            }, filepath_or_handle)

    def _handle_connection(self, socket, lock):
        try:
            cmd = socket.recv(decode=True)
            if cmd == 'setup':
                jid = socket.recv(decode=True)
                if jid in self.setup:
                    socket.send(self.setup[jid])
                    with lock:
                        self.__incomplete.add(jid)
                else:
                    socket.send('::ERR:Job ID {} not found'.format(jid))
            elif cmd == 'teardown':
                jid = socket.recv(decode=True)
                if jid in self.teardown:
                    socket.send(self.teardown[jid])
                    with lock:
                        self.__incomplete.remove(jid)
                else:
                    socket.send('::ERR:Job ID {} not found'.format(jid))
            else:
                socket.send('::ERR:Command {} not supported'.format(cmd))
        finally:
            socket.close()

    def serve(self, port: int):
        """
        Begins serving the setup/teardown data.
        RUNS IN FOREGROUND! Run in a separate thread if you do not want to block python.
        Automatically shuts down after all jobs have completed teardown
        """
        lock = threading.RLock()
        self.__incomplete = {*self.teardown}
        server = agutil.io.SocketServer(port)
        try:
            server.sock.settimeout(300)
            last_connection = time.monotonic()
            while len(self.__incomplete):
                try:
                    threading.Thread(
                        target=self._handle_connection,
                        args=(server.accept(), lock),
                        daemon=True
                    ).start()
                    last_connection = time.monotonic()
                except socket.timeout:
                    if (time.monotonic() - last_connection) > 3600:
                        # If the server has been idle for 1 hour, shut down
                        return
        finally:
            server.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'canine-manager',
        description='Setup and teardown manager for canine jobs'
    )

    parser.add_argument(
        'action',
        choices=['serve', 'setup', 'teardown']
    )

    parser.add_argument(
        'port',
        type=int
    )

    parser.add_argument(
        'target'
    )

    args = parser.parse_args()

    if args.action == 'serve':
        mgr = SetupManager()
        with open(args.target) as r:
            config = json.load(r)
        keys = {key for key in config['setup']} | {key for key in config['teardown']}
        for key in keys:
            mgr.add_job(
                key,
                config['setup'][key] if key in config['setup'] else '',
                config['teardown'][key] if key in config['teardown'] else ''
            )
        mgr.serve(args.port)
    else:
        socket = agutil.io.Socket('localhost', args.port)
        socket.send(args.action)
        socket.send(args.target)
        msg = socket.recv(decode=True)
        if msg.startswith('::ERR:'):
            raise ValueError(msg[6:])
        print(msg)
