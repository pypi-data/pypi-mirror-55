import ssl
from socket import socket, SOL_SOCKET, SO_REUSEADDR
from . import sslsocket


class ServerFactory:
    """
    A factory of asyncronous ssl sockets
    """

    def __init__(self, loop, ssl_context, header_length=10):
        self.loop = loop
        self.context = ssl_context
        self.header_length = header_length

    async def start_server(self, address, client_callback, addr_req=False,
                           pickle_data=False):

        server_socket = socket()
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind(address)
        server_socket.listen(5)
        print(f"\nListening for connections at {address[0]}:{address[1]}")

        while True:
            client_socket, client_address = await self.loop.sock_accept(server_socket)
            try:
                if not pickle_data:
                    ssl_client = sslsocket.ServerSocket(client_socket, self.context, self.header_length)
                else:
                    ssl_client = sslsocket.UPiServerSocket(client_socket, self.context, self.header_length)
            except IOError:
                client_socket.close()
                continue

            if addr_req is True:
                self.loop.create_task(client_callback(self.loop, ssl_client, client_address))
            else:
                self.loop.create_task(client_callback(self.loop, ssl_client))
