"""
Skill loader is a basic component where all skills get loaded.
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


class SkillLoader:  # (temp!) pylint: disable=C0115,R0903
    def __init__(self):
        module_path = os.path.dirname(os.path.abspath(__file__))
        tree = os.listdir(f"{module_path}/skills")

        # Filter out any files that contains double underscore
        # and doesn't end with '.py'.
        pattern = r"^[^__]*.py$"
        skills_tree = [s for s in tree if re.match(pattern, s)]

        self._skills = []

        for i in skills_tree:
            name = i.replace(".py", "")
            self._skills.append(
                self._get_skill_from_module(f"searchmate.skills.{name}")()
            )

        if len(self._skills) == 0:
            logging.warning("No skills were loaded, using fallback only.")

    def _get_skill_from_module(self, module: str) -> object:
        modules = importlib.import_module(module)

        skills = []
        for i in modules.__dict__:
            try:
                class_ = getattr(modules, i)

                # Append only if parent class' name is 'Skill'
                # and class has functions run() and suggestion().
                if class_.__bases__[0].__name__ == "Skill":
                    if not hasattr(class_, "run") or not hasattr(
                        class_, "suggestion"
                    ):
                        raise InvalidSkillException(
                            f"no function run() or suggestion() found \
in skill {class_.__name__}"
                        )
                    skills.append(class_)
            except AttributeError:
                continue

        if len(skills) != 1:
            raise InvalidSkillException(
                "exactly one skill class per module is required"
            )

        return skills[0]

    def get_suggestion(self, query: str) -> Optional[str]:
        try:
            words = query.split()
            keyword = words[0]
        except IndexError:
            return None

        for skill in self._skills:
            if keyword in skill.keywords:
                return skill.suggestion(" ".join(words[1:]))

        return None

    def run(self, query: str) -> Optional[str]:
        try:
            words = query.split()
            keyword = words[0]
        except IndexErrord:
            return None
            
        for skill in self._skills:
            if keyword in skill.keywords:
                return skill.run(" ".join(words[1:]))
