"""
SkillLoader is a basic component where all skills get loaded.
It checks 'skills/' directory in package home and loads all skills.
It also recognizes which skill should run with given input.
"""

import os
import re
import importlib
import logging

from typing import Optional


class InvalidSkillException(Exception):
    """Exception to throw when a skill is invalid."""

    def __init__(self, message):
        super().__init__(message)


class SkillLoader:
    """
    SkillLoader is a basic component where all skills get loaded.
    It checks 'skills/' directory in package home and loads all skills.
    It also recognizes which skill should run with given input.
    """

    def __init__(self):
        self._module_path = os.path.dirname(os.path.abspath(__file__))
        self._tree = os.listdir(f"{self._module_path}/skills")

        # Filter out any files that contains double underscore
        # and doesn't end with '.py'.
        self._pattern = r"^(?!_).*\.py$"
        self._skills_tree = [
            s for s in self._tree if re.match(self._pattern, s)
        ]

        self._skills = []

        for i in self._skills_tree:
            name = i.replace(".py", "")
            try:
                self._skills.append(
                    self._get_skill_from_module(f"searchmate.skills.{name}")()
                )
                logging.debug("SkillLoader - Loading skill %s.", name)
            except TypeError:
                logging.warning(
                    "SkillLoader - Couldn't load skill %s, "
                    "does it have run() and suggestion() "
                    "functions implemented?",
                    name,
                )

        if len(self._skills) == 0:
            logging.warning(
                "SkillLoader - No skills were loaded, using fallback only."
            )

    def _get_skill_from_module(self, module: str) -> object:
        modules = importlib.import_module(module)

        skills = []
        for i in modules.__dict__:
            try:
                class_ = getattr(modules, i)

                # Append only if parent class' name is 'Skill'.
                if class_.__bases__[0].__name__ == "Skill":
                    skills.append(class_)
            except AttributeError:
                continue

        if len(skills) != 1:
            raise InvalidSkillException(
                "exactly one skill class per module is required"
            )

        return skills[0]

    def get_suggestion(self, query: str) -> Optional[str]:
        """
        Searches for a skill and takes its suggesstion to a program.

        Args:
            query: Users' text input.

        Returns:
            Optional[str]: Skill's suggestion or None.
        """
        try:
            words = query.split()
            keyword = words[0].lower()
        except IndexError:
            return None

        for skill in self._skills:
            for skill_keyword in skill.keywords:
                if keyword in skill_keyword.lower():
                    return skill.suggestion(" ".join(words[1:]))

        return None

    def run(self, query: str) -> Optional[str]:
        """
        Searches for a skill and runs it.

        Args:
            query: Users' text input.

        Returns:
            Optional[str]: Skill's text output or None.
        """
        try:
            words = query.split()
            keyword = words[0]
        except IndexError:
            return None

        for skill in self._skills:
            if keyword in skill.keywords:
                return skill.run(" ".join(words[1:]))

        for skill in self._skills:
            try:
                if skill.fallback is True:
                    return skill.run(" ".join(words))
            except AttributeError:
                continue

        return None
