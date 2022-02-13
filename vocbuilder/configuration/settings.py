import json
import pathlib


class Settings:
    __is_initialized = False
    __settings = {}

    def __repr__(self):
        return "Settings[__is_initialized: {is_initialized}]".format(
            is_initialized=self.__is_initialized,
        )

    def __str__(self):
        return "Settings[{label}]".format(
            label="Loaded" if self.__is_initialized else "Not loaded",
        )

    def __init__(
        self,
        settings_file_path=None,
    ):
        if settings_file_path is not None:
            self._settings_file_path = settings_file_path
        else:
            self._settings_file_path = (
                pathlib.Path(__file__).parent / "settings.json"
            )

    def __load_file(self):
        with open(self._settings_file_path) as file:
            self.__settings = json.load(file)

    def initialize(self):
        self.__load_file()
        __is_initialized = True

    def get(
        self,
        key,
    ):
        return self.__settings.get(key, None)
