import socket
from address import Address, DEFAULT
from threading import Thread
import signal


class Server:

    def __init__(self, address=DEFAULT, port=DEFAULT):
        self.address = Address(address, port)  # init address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        try:
            print("-- Server startup --")
            self.socket.bind(self.address.to_tuple())
            self.socket.listen(5)
            print("Server is running...")
        except Exception as error:
            print("Server error:", error)  # DEBUG
            self.shutdown()
            print("-- Server shutdown --")
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
        Thread(target=self.handle_client).start()  # looping

    def signal_handler(self, sig, frame):
        print("SIGINT recieved")
        print("-- Server shutdown --")
        self.shutdown()
        exit(0)

    def handle_client(self):
        while self.running:
            client = self.socket.accept()
            self.clients.append(client)  # keep track of new client
            def func(): self.handle_recv(client)  # lambda
            Thread(target=func).start()  # looping
            print(f"-- Client [{client[1][1]}] has connected --")

    def broadcast(self, message):  # message is bytes
        for client in self.clients:
            clientsocket, _address = client
            try:
                clientsocket.send(message)
            except BrokenPipeError:
                self.clients.remove(client)

    def shutdown(self):
        self.running = False
        for client in self.clients:
            clientsocket, _address = client
            clientsocket.close()

    def handle_recv(self, client):
        clientsocket, address = client
        while self.running:
            try:
                msg = clientsocket.recv(1024)  # is bytes
            except Exception as error:
                print(f"Client [{address[1]}] had an unexpected erro: {error}")
                if client in self.clients:
                    self.clients.remove(client)
                return
            print(f"[{address[1]}]", msg.decode("utf-8"))
            self.broadcast(msg)


Server(port=5050)  # init
