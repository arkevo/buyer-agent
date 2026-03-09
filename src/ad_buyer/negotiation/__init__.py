# Author: Agent Range
# Donated to IAB Tech Lab

"""Multi-turn negotiation client with swappable strategy pattern."""

from .strategy import NegotiationStrategy, NegotiationContext
from .client import NegotiationClient
from .models import NegotiationSession, NegotiationRound, NegotiationResult, NegotiationOutcome

__all__ = [
    "NegotiationStrategy",
    "NegotiationContext",
    "NegotiationClient",
    "NegotiationSession",
    "NegotiationRound",
    "NegotiationResult",
    "NegotiationOutcome",
]
