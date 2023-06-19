"""This module manages configuration for Searchmate."""

import os
import configparser
import logging


class Config:
    """
    This class is a parent class for app and skills classes.

    Attributes:
        config_file: Path to a config file.
    """

    def __init__(self, config_file: str = None) -> None:
        """Class constructor, setups Config object."""
        if config_file is None:
            self.config_file = os.path.join(
                os.environ.get("SEARCHMATE_HOME")
                or os.path.join(
                    os.environ.get("APPDATA")
                    or os.environ.get("XDG_CONFIG_HOME")
                    or os.path.join(os.environ.get("HOME"), ".config"),
                    "searchmate",
                ),
                "config.ini",
            )
        else:
            self.config_file = config_file

        self._config = configparser.ConfigParser()
        self.load_config()

    def load_config(self) -> None:
        """Loads the config file to an object."""
        self._config.read(self.config_file)

    def save_config(self) -> None:
        """Saves object content to a config file."""
        os.makedirs(
            os.path.dirname(os.path.abspath(self.config_file)), exist_ok=True
        )
        with open(self.config_file, "w+", encoding="utf-8") as configfile:
            self._config.write(configfile)

        logging.debug("Config - Saving config to %s", self.config_file)

    def get(self, section: str, option: str) -> str:
        """
        Reads the setting value from an option name.

        Args:
            section: Section's name.
            option: Option's name.

        Returns:
            str: Option's saved value.
        """
        if not self._config.has_section(section) or not self._config.has_option(
            section, option
        ):
            self.set(section, option, "")
            self.save_config()

        value = self._config.get(section, option)

        if value == "":
            logging.warning("Config - No option %s:%s found", section, option)

        return value

    def set(self, section: str, option: str, value: str) -> None:
        """
        Sets option's value.

        Args:
            section: Section to choose option from.
            option: Option to change.
            value: Value to change to an option.
        """
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, option, value)


app_config = Config()
