import socket
import logging
import threading


log = logging.getLogger('sockio')


class TCP(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = None
        self._log = log.getChild('TCP({}:{})'.format(host, port))
        self._lock = threading.Lock()

    def open(self):
        with self._lock:
            if self.conn is not None:
                raise ConnectionError('socket already open')
            self.conn = socket.create_connection((self.host, self.port))
            self.conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
            self.fobj = self.conn.makefile('rwb', 0)

    def close(self):
        with self._lock:
            if self.conn is not None:
                self.conn.shutdown()
                self.conn.close()
            self.conn = None
            self.fobj = None

    def write(self, data):
        with self._lock:
            return self.fobj.write(data)

    def read(self, n=-1):
        with self._lock:
            return self.fobj.read(n)

    def readline(self):
        with self._lock:
            return self.fobj.readline()

    def writelines(self, lines):
        with self._lock:
            return self.fobj.writelines(lines)

    def write_readline(self, data):
        with self._lock:
            self.fobj.write(data)
            return self.fobj.readline()

    def writelines_readlines(self, lines, n=None):
        if n is None:
            n = len(lines)
        with self._lock:
            self.fobj.writelines(lines)
            return [self.fobj.readline() for i in range(n)]
