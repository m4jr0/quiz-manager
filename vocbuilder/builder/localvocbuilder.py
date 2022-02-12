import pathlib

import builder.vocbuilder as voc


class LocalVocBuilder(voc.AsbtractVocBuilder):
    def __init__(self, training_file_path=None):
        if training_file_path is not None:
            self._training_file_path = training_file_path
        else:
            self._training_file_path = (
                pathlib.Path(__file__).parent / "training.csv"
            )

    def __repr__(self):
        return "LocalVocBuilder[len(_voc): {voc_len}]".format(
            voc_len=len(self._voc) if self._voc is not None else 0,
        )

    def __str__(self):
        return "LocalVocBuilder[{word_count} word(s)]".format(
            word_count=len(self._voc) if self._voc is not None else 0,
        )

    @staticmethod
    def __get_value(line, start_index=0):
        char_count = len(line)

        if start_index > char_count:
            return None

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

    def _build_vocabulary(self, grades, indexes):
        self._voc = []

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
                word, cursor = self.__get_value(line, cursor)
                answer, cursor = self.__get_value(line, cursor)

                index = int(index)

                if not word or not answer:
                    break

                if grades is not None and grade.lower() not in grades:
                    break

                is_contained = indexes is None

                if not is_contained:
                    for interval in indexes:
                        if interval.contains(index):
                            is_contained = True
                            break

                if not is_contained:
                    continue

                self._voc.append(
                    {
                        "index": index,
                        "grade": grade,
                        "word": word.strip(),
                        "answer": answer.strip(),
                    }
                )
