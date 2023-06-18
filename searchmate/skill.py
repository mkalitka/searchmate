"""Abstract skill class."""

from abc import ABC, abstractmethod


class Skill(ABC):
    """
    Abstract skill class, needs to be a parent of each skill.

    Attributes:
        query: Users' text input.
    """

    def __init__(self, query: str) -> None:
        self.query = query
        self.keywords = []

    @abstractmethod
    def run(self) -> str:
        """
        Code to be executed when running skill.

        Returns:
            str: Text to display after skill runs.
        """
        return None

    @abstractmethod
    def suggestion(self) -> str:
        """
        What to display before executing skill.

        Returns:
            str: Text to display before skill runs.
        """
        return None
