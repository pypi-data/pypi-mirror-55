from types import coroutine
from collections import deque
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


@coroutine
def read_wait(sock):
    yield 'read_wait', sock


@coroutine
def write_wait(sock):
    yield 'write_wait', sock


class EventLoop:

    def __init__(self):
        self.ready = deque()
        self.selector = DefaultSelector()

    async def sock_recv(self, sock):
        await read_wait(sock)
        return sock.recv()

    async def sock_accept(self, sock):
        await read_wait(sock)
        return sock.accept()

    async def sock_sendall(self, sock, data):
        try:
            sock.send_all(data)
        except BlockingIOError:
            await write_wait(sock)

    def read_wait(self, sock):
        self.selector.register(sock, EVENT_READ, self.current_task)

    def write_wait(self, sock):
        self.selector.register(sock, EVENT_WRITE, self.current_task)

    def create_task(self, coro):
        self.ready.append(coro)

    def run_forever(self):
        while True:
            while not self.ready:
                events = self.selector.select()
                for key, _ in events:
                    self.ready.append(key.data)
                    self.selector.unregister(key.fileobj)

            while self.ready:
                self.current_task = self.ready.popleft()
                try:
                    # Run the generator to the yield
                    op, *args = self.current_task.send(None)

                    # Run the task -> e.g getattr(self, sock_recv)()
                    getattr(self, op)(*args)  # Sneaky method call
                except StopIteration:
                    continue
