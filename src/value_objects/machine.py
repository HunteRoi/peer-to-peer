from dataclasses import dataclass


@dataclass
class Machine:
    """Represents a machine in the network."""

    ip_address: str
    port: int
