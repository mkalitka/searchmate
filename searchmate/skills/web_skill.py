"""Web skill."""

from typing import Optional

import webbrowser

from searchmate.skill import Skill


class WebSkill(Skill):
    """
    Web skill, it launches web search with given input as fallback.
    """

    def __init__(self) -> None:
        super().__init__()
        self.fallback = True

    def run(self, query: str) -> Optional[str]:
        """
        Launches web search.

        Attributes:
            query: Users' text input.

        Returns:
            str: Evaluated text to display after skill runs.
        """

        webbrowser.open(f"https://www.google.com/search?q={query}")

        return {
            "widget_type": "exit",
            "message": ""
        }

    def suggestion(self, query: str) -> Optional[str]:
        """
        Evaluates math expression.

        Attributes:
            query: Users' text input.

        Returns:
            str: Evaluated text to display before skill runs.
        """
        return None
        
