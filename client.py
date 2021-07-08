import socket
from address import Address, DEFAULT
from threading import Thread
import time
import signal


class Client:

    def __init__(self, address=DEFAULT, port=DEFAULT):
        self.address = Address(address, port)  # init address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:  # try to connect to server
            self.socket.connect(self.address.to_tuple())
            print(f"-- Connected to server [{self.address.to_tuple()[0]}] --")
        except ConnectionRefusedError:
            print("Server could not be found!")
            print("-- Exited program --")
            self.shutdown()
            exit()

        self.connected = True
        signal.signal(signal.SIGINT, self.signal_handler)
        Thread(target=self.handle_input).start()  # looping
        Thread(target=self.handle_recv).start()  # looping

    def signal_handler(sig, frame):
        print("SIGINT recieved")
        print("-- Client connections closed --")
        print("-- Exited program --")
        self.shutdown()
        exit(0)

    def handle_input(self):  # threaded
        while self.connected:
            msg = input("Enter message: ")
            self.socket.send(bytes(msg, "utf-8"))
            time.sleep(1)

    def handle_recv(self):
        while self.connected:
            try:
                msg = self.socket.recv(1024).decode("utf-8")
                if msg == "":
                    print("\n-- Disconnected from server --")
                    self.shutdown()
                    return
                print("\n|", msg)  # from server
            except ConnectionResetError:
                self.shutdown()
                print("\n-- Disconnected from server --")

    def shutdown(self):
        self.connected = False
        self.socket.close()


Client(port=5050, address="vps.i-h.no")  # init
