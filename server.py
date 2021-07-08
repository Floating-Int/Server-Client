import socket
from address import Address, DEFAULT
from threading import Thread


class Server:

    def __init__(self, address=DEFAULT, port=DEFAULT):
        self.address = Address(address, port)  # init adress
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
        Thread(target=self.handle_client).start()  # looping

    def handle_client(self):
        while self.running:
            client = self.socket.accept()
            self.clients.append(client)  # keep track of new client
            def func(): self.handle_recv(client)  # lambda
            Thread(target=func, name="This").start()  # looping
            print(f"-- Client [{client[1][1]}] has connected --")

    def broadcast(self, message):  # message is bytes
        for client in self.clients:
            clientsocket, _adress = client
            clientsocket.send(message)

    def shutdown(self):
        self.running = False
        for client in self.clients:
            clientsocket, _adress = client
            clientsocket.close()

    # def handle_recv(self):
    #    while self.running:  # TODO: handle recv on each client in Threads
    #        if len(self.clients) == 0:
    #            continue
    #        for client in self.clients:
    #            clientsocket, address = client
    #            msg = clientsocket.recv(1024)  # is bytes
    #            print(f"[{address[1]}]", msg.decode("utf-8"))
    #            self.broadcast(msg)

    def handle_recv(self, client):
        clientsocket, address = client
        print("Now", address)
        while self.running:
            msg = clientsocket.recv(1024)  # is bytes
            print(f"[{address[1]}]", msg.decode("utf-8"))
            self.broadcast(msg)


Server(port=5050)  # init
