from unittest.mock import MagicMock, patch
from pytest import fixture, raises

from src.services.node import Node
from src.exceptions.not_a_machine_error import NotAMachineError
from src.value_objects.machine import Machine


class TestNode:
    """Test suite for the Node"""

    @fixture(name="node_machine")
    def create_node_machine(self) -> Machine:
        """Creates a free node"""
        return Machine("10.0.0.3", 1024)

    @patch("socket.socket")
    def test_invite_to_network_raises_exception_given_no_target_node(
        self, mock_socket: MagicMock
    ):
        """Validates that an exception is raised when no target node is given"""
        mock_socket.return_value = mock_socket
        mock_socket.getsockname.return_value = ["10.0.0.2", 1024]
        node = Node()

        with raises(NotAMachineError):
            node.invite_to_network(None)

    @patch("socket.socket")
    def test_invite_to_network_returns_false_when_target_node_has_parent(
        self, mock_socket: MagicMock, node_machine: Machine
    ):
        """Validates that it is not possible to invite a node to the network
        when the target node already has a parent"""
        mock_socket.return_value = mock_socket
        mock_socket.getsockname.return_value = ["10.0.0.2", 1024]
        mock_socket.recvfrom.return_value = (
            b"refuse",
            (node_machine.ip_address, node_machine.port),
        )
        node_with_parent = node_machine
        node = Node()

        is_added = node.invite_to_network(node_with_parent)

        assert not is_added

    @patch("socket.socket")
    def test_invite_to_network_returns_true_given_a_node_without_parent(
        self, mock_socket: MagicMock, node_machine: Machine
    ):
        """Validates that a node can be initialized when transmitting with a parent"""
        mock_socket.return_value = mock_socket
        mock_socket.getsockname.return_value = ["10.0.0.2", 1024]
        mock_socket.recvfrom.return_value = (
            b"accept",
            (node_machine.ip_address, node_machine.port),
        )
        node = Node()

        is_added = node.invite_to_network(node_machine)

        assert is_added

    @patch("socket.socket")
    def test_invite_to_network_returns_false_in_case_of_error(
        self, mock_socket: MagicMock, node_machine: Machine
    ):
        """Validates that a node is resistent to network issues"""
        mock_socket.return_value = mock_socket
        mock_socket.getsockname.side_effect = Exception("Network error")
        node = Node()

        is_added = node.invite_to_network(node_machine)

        assert not is_added
