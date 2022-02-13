import pathlib

import quizmanager.quizmanager as quiz


class CSVQuizManager(quiz.AsbtractQuizManager):
    def __init__(self, quiz_file_path=None, is_reversed=False):
        super().__init__(is_reversed)

        if quiz_file_path is not None:
            self.__quiz_file_path = quiz_file_path
        else:
            self.__quiz_file_path = pathlib.Path(__file__).parent / "quiz.csv"

    def __repr__(self):
        return "CSVQuizManager[len(_quiz): {quiz_len}, __quiz_file_path: {quiz_file_path}, _is_reversed: {is_reversed}]".format(
            quiz_len=len(self._quiz) if self._quiz is not None else 0,
            quiz_file_path=self.__quiz_file_path,
            is_reversed=self._is_reversed,
        )

    def __str__(self):
        return "CSVQuizManager[{question_count} question(s){reverse_label} [{quiz_file_path}]]".format(
            question_count=len(self._quiz) if self._quiz is not None else 0,
            reverse_label="" if not is_reversed else " (reversed)",
            quiz_file_path=self.__quiz_file_path,
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

    def _build_quiz(
        self,
        grades,
        indexes,
    ):
        self.reset()

        with open(
            self.__quiz_file_path,
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
                notes, cursor = self.__get_value(line, cursor)
                index = int(index)

                self._handle_question(
                    grades,
                    indexes,
                    index,
                    grade,
                    question,
                    answer,
                    notes,
                )
