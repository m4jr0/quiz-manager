import pathlib

import builder.vocbuilder as voc
import handler.gdrivehandler as gdrive


class GSheetVocBuilder(voc.AsbtractVocBuilder):
    __gdrive_handler = None
    __sheet_id = None
    __range = None

    def __init__(self, token_path, sheet_id, range=None):
        self.__gdrive_handler = gdrive.GDriveHandler(
            token_path, gdrive.GDriveHandler.SCOPE_SHEET_READONLY
        )

        self.__sheet_id = sheet_id
        self.__range = range

    def __repr__(self):
        return "GSheetVocBuilder[len(_voc): {voc_len}]".format(
            voc_len=len(self._voc) if self._voc is not None else 0,
        )

    def __str__(self):
        return "GSheetVocBuilder[{word_count} word(s)]".format(
            word_count=len(self._voc) if self._voc is not None else 0,
        )

    def initialize(self, raw_grades=None, raw_indexes=None):
        self.__gdrive_handler.initialize()
        super().initialize(raw_grades, raw_indexes)

    def _build_vocabulary(self, grades, indexes):
        self.reset()

        values = self.__gdrive_handler.fetch_values(
            self.__sheet_id,
            self.__range,
        )

        is_first = True

        for row in values:
            if is_first:
                is_first = False
                continue

            if len(row) < 4:
                continue

            index = int(row[0])
            grade = row[1]
            word = row[2]
            answer = row[3]

            self._handle_word(
                grades,
                indexes,
                index,
                grade,
                word,
                answer,
            )
