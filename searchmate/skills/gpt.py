"""GPT skill."""

from typing import Optional

from searchmate.skill import Skill


class GPTSkill(Skill):
    """
    GPT skill, makes chatting with GPT available in SearchMate.
    """

    def __init__(self) -> None:
        super().__init__()
        self.keywords = ["gpt"]

    def run(self, query: str) -> Optional[str]:
        """
        Code to be executed when running skill.

        Arguments:
            query: Users' text input.

        Returns:
            str: Text to display after skill runs.
        """
        return f"Enter: {query}"

    def suggestion(self, query: str) -> Optional[str]:
        """
        What to display before executing skill.

        Arguments:
            query: Users' text input.

        Returns:
            str: Text to display before skill runs.
        """
        return query
