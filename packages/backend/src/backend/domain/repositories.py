from abc import ABC, abstractmethod
from typing import List
from backend.domain.entities import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    def load_transactions(self) -> List[Transaction]:
        """Load transactions from the data source."""
        pass
