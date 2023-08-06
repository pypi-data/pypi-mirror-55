from .evloop import EventLoop
from .server_factory import ServerFactory
from .sslsocket import ServerSocket, ClientSocket, UPiServerSocket, UPiClientSocket
from .sslsocket import (hostname, decode, encode, loads, dumps)
from .io import SingleInstance, get_idle_duration

__all__ = ['EventLoop', 'ServerSocket', 'ClientSocket',
           "UPiServerSocket", "UPiClientSocket" 'hostname',
           'decode', 'encode', 'loads', 'dumps', 'SingleInstance',
           'get_idle_duration']


class PickleableFile(object):
    def __init__(self, filename, mode='rb'):
        self.filename = filename
        self.mode = mode
        self.file = open(filename, mode)

    def __getstate__(self):
        state = dict(filename=self.filename, mode=self.mode, closed=self.file.closed)
        if not self.file.closed:
            state['filepos'] = self.file.tell()
        return state

    def __setstate__(self, state):
        self.filename = state['filename']
        self.mode = state['mode']
        self.file = open(self.filename, self.mode)
        if state['closed']:
            self.file.close()
        else:
            self.file.seek(state['filepos'])

    def __getattr__(self, attr):
        return getattr(self.file, attr)
