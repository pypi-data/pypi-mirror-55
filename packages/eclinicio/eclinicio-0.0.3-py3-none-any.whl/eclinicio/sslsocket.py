import socket
import pickle
import ssl


def hostname():
    """Return ip address of this computer on the network"""
    try:
        return socket.gethostbyname_ex(socket.gethostname())[2][0]
    except socket.gaierror:
        return socket.gethostbyname_ex('localhost')[2][0]


def decode(data):
    return data.decode('utf-8')


def encode(data):
    return data.encode("utf-8")


def dumps(obj):
    return pickle.dumps(obj, protocol=-1)


def loads(obj):
    return pickle.loads(obj)


class ServerSocket:
    def __init__(self, sock, context, header_length=10):
        self.header_length = header_length
        self.sock = context.wrap_socket(sock, server_side=True)

    def __enter__(self):
        return self.sock

    def __exit__(self, exec_type, exc_value, tb):
        self.close()

    def compose_message(self, message: object):
        """Compose a message from python object"""
        pickled_message = dumps(message)
        message_header = encode(f"{len(pickled_message):<{self.header_length}}")
        return message_header + pickled_message

    def send(self, message):
        return self.send_all(message)

    def send_all(self, message):
        """Send data to a remote peer"""
        pickled_message = self.compose_message(message)
        return self.sock.sendall(pickled_message)

    def receive_message(self):
        try:
            message_header = self.sock.recv(self.header_length)
            if not len(message_header):
                return False

            message_length = int(decode(message_header).strip())

            data = bytearray()
            while len(data) < message_length:
                packet = self.sock.recv(message_length - len(data))
                if not packet:
                    break
                data.extend(packet)

            return {
                "header": message_header,
                "data": loads(data)
            }
        except:
            return {}

    def recv(self):
        message = self.receive_message()
        if message:
            return message['data']

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            return self.sock.close()
        except OSError:
            pass

    def connect(self, address):
        raise TypeError("Invalid call on server-side socket !")

    def __getattr__(self, name):
        return getattr(self.sock, name)


class ClientSocket(ServerSocket):
    """
    Executes at the client side.
    """

    def __init__(self, context=None, header_length=10):
        if context is None:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        else:
            ssl_context = context
        self.sock = ssl_context.wrap_socket(socket.socket())
        self.header_length = header_length

    def connect(self, address):
        return self.sock.connect(address)

    def accept(self):
        raise TypeError("Invalid call on client-side socket !")


class UPiClientSocket(ClientSocket):
    """SSL socket for sending unpickled data"""

    def compose_message(self, message: bytes):
        """Compose a message from python object"""
        message_header = encode(f"{len(message):<{self.header_length}}")
        return message_header + message

    def send(self, message: bytes):
        return self.send_all(message)

    def send_all(self, message: bytes):
        """Send data to a remote peer"""
        msg = self.compose_message(message)
        return self.sock.sendall(msg)

    def receive_message(self):
        try:
            message_header = self.sock.recv(self.header_length)
            if not len(message_header):
                return False

            message_length = int(decode(message_header).strip())

            data = bytearray()
            while len(data) < message_length:
                packet = self.sock.recv(message_length - len(data))
                if not packet:
                    break
                data.extend(packet)

            return {
                "header": message_header,
                "data": data
            }
        except:
            return {}

    def yield_recv(self, file_size):
        try:
            recv_bytes = 0
            while recv_bytes < file_size:
                packet = self.sock.recv(4096)
                if not packet:
                    break
                yield packet
        except:
            yield False

    def recv(self):
        return self.sock.recv(1024)


class UPiServerSocket(ServerSocket):
    """SSL socket for sending unpickled data"""

    def send(self, message: bytes):
        return self.send_all(message)

    def send_all(self, message: bytes):
        """Send data to a remote peer"""
        return self.sock.sendall(msg)
