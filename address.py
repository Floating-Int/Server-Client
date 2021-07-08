import socket


DEFAULT = None


class Address:
    """
    Datastructure:
    - Has default hostname and port
    - Use .to_tuple() to convert to tuple
    """

    def __init__(self, hostname=DEFAULT, port=DEFAULT):
        self.hostname = socket.gethostname() if hostname == DEFAULT else hostname
        self.port = 5050 if port == DEFAULT else port

    def to_tuple(self):
        """
        Returns a tuple containing hostname and port
        """
        return (self.hostname, self.port)
