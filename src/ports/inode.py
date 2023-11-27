from abc import ABC, abstractmethod

from src.value_objects.machine import Machine


class INode(ABC):
    """Interface for nodes in the network"""

    @abstractmethod
    def invite_to_network(self, node: Machine) -> bool:
        """Invites a node to the network"""
