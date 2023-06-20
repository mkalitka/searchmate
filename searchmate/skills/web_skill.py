"""Web skill."""

from typing import Optional, Dict

import webbrowser

from searchmate.skill import Skill


class WebSkill(Skill):
    """
    Web skill, it launches web search with given input as fallback.
    """

    def __init__(self) -> None:
        super().__init__()
        self.fallback = True

    def run(self, query: str) -> Optional[Dict[str, str]]:
        """
        Launches web search.

        Args:
            query: Users' text input.

        Returns:
            Optional[Dict[str, str]]: Evaluated text to display after skill runs.
        """

        webbrowser.open(f"https://www.google.com/search?q={query}")

        return {"widget_type": "exit", "message": ""}

    def suggestion(self, query: str) -> Optional[Dict[str, str]]:
        """
        Evaluates math expression.

        Args:
            query: Users' text input.

        Returns:
            Optional[Dict[str, str]]: Suggestion to display.
        """
        return None
