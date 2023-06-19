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

        self._drummer_joke = (
            "Idzie perkusista przez las, idzie, odwraca się, "
            "patrzy, a tam wielka stopa. Ba dum tss."
        )

    def run(self, query: str) -> Optional[str]:
        """
        Evaluates math expression.

        Attributes:
            query: Users' text input.

        Returns:
            str: Evaluated text to display after skill runs.
        """
        return self.suggestion(query)

    def suggestion(self, query: str) -> Optional[str]:
        """
        Evaluates math expression.

        Attributes:
            query: Users' text input.

        Returns:
            str: Evaluated text to display before skill runs.
        """
        if not query or query.isspace():
            return None

        try:
            result = cexprtk.evaluate_expression(query, {})

            if result == int(result):
                result = str(int(result))
        except OverflowError:
            result = self._drummer_joke
        except:  # pylint: disable=W0702
            return self.suggestion(query[:-1])

        return {
            "widget_type": "plain",
            "message": result,
        }
