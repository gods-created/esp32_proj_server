from abc import ABC, abstractmethod

from typing import Optional

class BaseSerializer(ABC):
    @abstractmethod
    def insert(self, value: str) -> dict:
        pass 

    @abstractmethod
    def select(self, id: Optional[str] = None) -> dict:
        pass 

    @abstractmethod
    def delete(self, id: Optional[str] = None) -> dict:
        pass 