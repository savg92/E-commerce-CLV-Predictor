"""Domain repository interfaces for the E-commerce CLV Predictor."""

from abc import ABC, abstractmethod
from typing import List
from backend.domain.entities import Transaction

class TransactionRepository(ABC):
    """Abstract interface for loading transactional data."""

    @abstractmethod
    def load_transactions(self) -> List[Transaction]:
        """Load transactions from the data source."""
        pass
