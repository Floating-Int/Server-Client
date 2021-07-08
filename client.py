import socket
from address import Address, DEFAULT
from threading import Thread
import time


class Client:

    def __init__(self, address=DEFAULT, port=DEFAULT):
        self.adress = Address(address, port)  # init adress
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:  # try to connect to server
            self.socket.connect(self.adress.to_tuple())
            print(f"-- Connected to server [{self.adress.to_tuple()[0]}] --")
        except ConnectionRefusedError:
            print("Server could not be found!")
            print("-- Exited program --")
            self.shutdown()
            exit()

        self.connected = True
        Thread(target=self.handle_input).start()  # looping
        Thread(target=self.handle_recv).start()  # looping

    def handle_input(self):  # threaded
        while self.connected:
            msg = input("Enter message: ")
            self.socket.send(bytes(msg, "utf-8"))
            time.sleep(1)

    def handle_recv(self):
        while self.connected:
            try:
                msg = self.socket.recv(1024)
                print("| ", msg.decode("utf-8"))  # from server
            except ConnectionResetError:
                self.shutdown()
                print("\n-- Disconnected from server --")

    def shutdown(self):
        self.connected = False
        self.socket.close()


Client(port=5050)  # init
