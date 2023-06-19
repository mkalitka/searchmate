"""Abstract skill class."""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class Skill(ABC):
    """
    Abstract skill class, needs to be a parent of each skill.
    """

    def __init__(self) -> None:
        self.keywords = []

    @abstractmethod
    def run(self, query: str) -> Optional[Dict[str, str]]:
        """
        Code to be executed when running skill.

        Args:
            query: Users' text input.

        Returns:
            str: Text to display after skill runs.
        """
        return None

    @abstractmethod
    def suggestion(self, query: str) -> Optional[Dict[str, str]]:
        """
        What to display before executing skill.

        Args:
            query: Users' text input.

        Returns:
            str: Text to display before skill runs.
        """
        return None
