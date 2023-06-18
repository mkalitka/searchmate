"""
Skill loader is a basic component where all skills get loaded.
It checks 'skills/' directory in package home and loads all skills.
It also recognizes which skill should run with given input.
"""

import os
import re
import importlib
import logging


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

                if not hasattr(class_, "run") or not hasattr(
                    class_, "suggestion"
                ):
                    raise InvalidSkillException(
                        f"no functions run() and suggestion() found in skill {class_.__name__}"
                    )

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
