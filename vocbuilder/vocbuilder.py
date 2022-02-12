from pathlib import Path
from random import randrange

from misc.interval import Interval


class VocBuilder:
    GRADE_ALL = "all"
    GRADE_SERF = "serf"
    GRADE_KNIGHT = "knight"
    GRADE_WIZARD = "wizard"
    GRADE_KING = "king"

    GRADES = [
        GRADE_SERF,
        GRADE_KNIGHT,
        GRADE_WIZARD,
        GRADE_KING,
    ]

    __voc = None
    __dir = Path(__file__).parent

    def __repr__(self):
        return "VocBuilder[len(__voc): {voc_len}]".format(
            voc_len=len(self.__voc) if self.__voc is not None else 0,
        )

    def __str__(self):
        return "VocBuilder [{word_count} word(s)]".format(
            word_count=len(self.__voc) if self.__voc is not None else 0,
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

    @classmethod
    def __get_grades(cls, raw_grades):
        if raw_grades is None:
            return None

        grades = None

        for raw_grade in raw_grades:
            grade = raw_grade.lower() if raw_grade is not None else None

            if grade == cls.GRADE_ALL:
                grades = None
                break

            elif grade not in cls.GRADES:
                raise ValueError(
                    "Invalid grade: {grade}".format(
                        grade=raw_grade,
                    )
                )

            if grades is None:
                grades = []

            grades.append(grade)

        return grades

    def __get_indexes(self, raw_indexes):
        if raw_indexes is None:
            return None

        indexes = None

        for raw_interval in raw_indexes:
            numbers = raw_interval.split("-")
            number_count = len(numbers)

            if number_count <= 0 or number_count > 2:
                raise ValueError(
                    "Invalid interval: {interval}".format(
                        interval=raw_interval,
                    )
                )

            if indexes is None:
                indexes = []

            try:
                x = numbers[0]
                x = int(x)

            except ValueError:
                raise ValueError(
                    "Invalid interval value: {x}".format(
                        x=x,
                    )
                )

            try:
                if number_count == 1:
                    y = x

                else:
                    y = numbers[1]
                    y = int(y)

            except ValueError:
                raise ValueError(
                    "Invalid interval value: {y}".format(
                        y=y,
                    )
                )

            indexes.append(Interval(x, y))

        return indexes

    def __build_vocabulary(self, grades, indexes):
        self.__voc = []

        with open(
            "{dir}/../training.csv".format(
                dir=self.__dir,
            ),
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

                self.__voc.append(
                    {
                        "index": index,
                        "grade": grade,
                        "word": word.strip(),
                        "answer": answer.strip(),
                    }
                )

    def initialize(self, raw_grades=None, raw_indexes=None):
        grades = self.__get_grades(raw_grades)
        indexes = self.__get_indexes(raw_indexes)
        self.__build_vocabulary(
            grades,
            indexes,
        )

    def train(
        self,
        grades=None,
    ):
        if self.__voc is None:
            print("Vocabulary not initialized.")
            return

        count = len(self.__voc)

        if count <= 0:
            print("Nothing to see here...")
            return

        print(
            "{count} word(s) to review!".format(
                count=count,
            )
        )

        while count > 0:
            descr = self.__voc.pop(randrange(count))
            count -= 1

            print(
                "Word #{index}:\n{word} [{grade}]".format(
                    index=descr["index"],
                    word=descr["word"],
                    grade=descr["grade"],
                )
            )

            input()

            print("Answer:\n{answer}\n".format(answer=descr["answer"]))
            print("**************************************************\n")

        print("You did it!")
