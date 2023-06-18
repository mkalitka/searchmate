"""Abstract skill class."""

from searchmate.skill import Skill


class GPTSkill(Skill):
    """
    Abstract skill class, needs to be a parent of each skill.

    Attributes:
        query: Users' text input.
    """

    def __init__(self, query: str) -> None:
        super().__init__(query)
        self.keywords = ["gpt"]

    def run(self) -> str:
        """
        Code to be executed when running skill.

        Returns:
            str: Text to display after skill runs.
        """
        return None

    def suggestion(self) -> str:
        """
        What to display before executing skill.

        Returns:
            str: Text to display before skill runs.
        """
        return None
