import pathlib

import builder.vocbuilder as voc


class CSVVocBuilder(voc.AsbtractVocBuilder):
    def __init__(self, training_file_path=None, is_reversed=False):
        super().__init__(is_reversed)

        if training_file_path is not None:
            self._training_file_path = training_file_path
        else:
            self._training_file_path = (
                pathlib.Path(__file__).parent / "training.csv"
            )

    def __repr__(self):
        return "CSVVocBuilder[len(_voc): {voc_len}, _is_reversed: {is_reversed}]".format(
            voc_len=len(self._voc) if self._voc is not None else 0,
            is_reversed=self._is_reversed,
        )

    def __str__(self):
        return (
            "CSVVocBuilder[{question_count} question(s){reverse_label}]".format(
                question_count=len(self._voc) if self._voc is not None else 0,
                reverse_label="" if not is_reversed else " (reversed)",
            )
        )

    @staticmethod
    def __get_value(
        line,
        start_index=0,
    ):
        char_count = len(line)

        if start_index > char_count - 1:
            return None, start_index

        index = start_index
        separator_quote = '"'
        separator = ","
        to_add = 1

        if line[index] == separator_quote:
            separator = separator_quote
            to_add = 2
            start_index += 1
            index += 1

        while index < char_count and line[index] != separator:
            index += 1

        return (line[start_index:index], index + to_add)

    def _build_vocabulary(
        self,
        grades,
        indexes,
    ):
        self.reset()

        with open(
            self._training_file_path,
            "r",
        ) as file:
            results = []
            is_first = True

            for line in file:
                if is_first:
                    is_first = False
                    continue

                index, cursor = self.__get_value(line)
                grade, cursor = self.__get_value(line, cursor)
                question, cursor = self.__get_value(line, cursor)
                answer, cursor = self.__get_value(line, cursor)
                index = int(index)

                self._handle_question(
                    grades,
                    indexes,
                    index,
                    grade,
                    question,
                    answer,
                )
