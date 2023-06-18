"""Math skill."""

from typing import Optional

import cexprtk

from searchmate.skill import Skill

class MathSkill(Skill):
    """
    Math skill, it evaluates string to a math value.
    """

    def __init__(self) -> None:
        super().__init__()
        self.keywords = ["math"]

    def run(self, query: str) -> Optional[str]:
        """
        Code to be executed when running skill.

        Attributes:
            query: Users' text input.

        Returns:
            str: Text to display after skill runs.
        """
        return self.suggestion(query)

    def suggestion(self, query: str) -> Optional[str]:
        """
        What to display before executing skill.

        Attributes:
            query: Users' text input.

        Returns:
            str: Text to display before skill runs.
        """
        result = cexprtk.evaluate_expression(query, {})

        try:
            if result == int(result):
                return str(int(result))
        except Exception:
            return "Idzie perkusista przez las, idzie, odwraca się, \
patrzy, a tam wielka stopa. Ba dum tss."

        return str(result)
