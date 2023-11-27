import socket

from src.exceptions.not_a_machine_error import NotAMachineError
from src.ports.inode import INode
from src.value_objects.machine import Machine


class Node(INode):
    """Node is a representation of a node in the network"""

    inner_socket: socket.socket
    inner_machine: Machine
    parent: Machine
    children: list[Machine]

    def __init__(self):
        try:
            self.inner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.inner_socket.bind(("", 0))
            self.inner_socket.listen()

            self.inner_machine = Machine(
                self.inner_socket.getsockname()[0], self.inner_socket.getsockname()[1]
            )
        except:
            self.inner_machine = Machine("", 0)
        self.parent = None
        self.children = []

    def invite_to_network(self, node: Machine) -> bool:
        """Invites a node to the network"""

        if (node is None) or (not isinstance(node, Machine)):
            raise NotAMachineError("Invalid node")

        try:
            self.inner_socket.connect((node.ip_address, node.port))
            self.inner_socket.sendto(b"invite", (node.ip_address, node.port))
            (data, _) = self.inner_socket.recvfrom(1024, (node.ip_address, node.port))
            self.inner_socket.close()
        except:
            return False

        if data == b"accept":
            self.children.append(node)
            return True
        return False
