import sys
import select
import socket
import threading

try:
    import selectors
except ImportError:
    import selectors34 as selectors


class EventLoop(object):

    class Channel:

        def __init__(self):
            self.reader, self.writer = os.pipe()

        def fileno(self):
            return self.reader

        def send(self, msg):
            os.write(self.writer, msg)

        def read(self):
            return os.read(self.reader, 4096)

        def close(self):
            os.close(self.reader)
            os.close(self.writer)

        def send_stop(self):
            self.send(b'STOP\n')


    def __init__(self):
        self.selector = None
        self.channel = None

    def register(self, fileobj, events, data=None):
        return self.selector.register(fileobj, events, data=data)

    def unregister(self, fileobj):
        return self.selector.unregister(fileobj)

    def start(self):
        self.channel = self.Channel()
        self.selector = selectors.DefaultSelector()
        self.register(self.channel, selectors.EVENT_READ)
        self.task = threading.Thread(name='IOTH', target=self._run)
        self.task.daemon = True
        self.task.start()

    def _run(self):
        stop = False
        while not stop:
            events = self.selector.select()
            for event, mask in events:
                if event.fileobj == self.channel:
                    msg = self.channel.read()
                    if msg == b'STOP\n':
                        stop = True
                        continue
                    raise NotImplementedError
                cb = event.data
                try:
                    

    def stop(self):
        pass

    def tcp(self, host, port):
        pass


DefaultEventLoop = EventLoop()
TCP = DefaultEventLoop.tcp

