import abc

from random import randrange

from misc.interval import Interval


class AsbtractVocBuilder(metaclass=abc.ABCMeta):
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

    _voc = None

    def __repr__(self):
        return "AbstractVocBuilder[len(_voc): {voc_len}]".format(
            voc_len=len(self._voc) if self._voc is not None else 0,
        )

    def __str__(self):
        return "AbstractVocBuilder[{word_count} word(s)]".format(
            word_count=len(self._voc) if self._voc is not None else 0,
        )

    @classmethod
    def __get_grades(
        cls,
        raw_grades,
    ):
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

    def __get_indexes(
        self,
        raw_indexes,
    ):
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

    @abc.abstractmethod
    def _build_vocabulary(
        self,
        grades,
        indexes,
    ):
        return

    def initialize(
        self,
        raw_grades=None,
        raw_indexes=None,
    ):
        grades = self.__get_grades(raw_grades)
        indexes = self.__get_indexes(raw_indexes)
        self._build_vocabulary(
            grades,
            indexes,
        )

    def reset(self):
        self._voc = []

    def _handle_word(
        self,
        grades,
        indexes,
        index,
        grade,
        word,
        answer,
    ):
        if not word or not answer:
            return

        if grades is not None and grade.lower() not in grades:
            return

        is_contained = indexes is None

        if not is_contained:
            for interval in indexes:
                if interval.contains(index):
                    is_contained = True
                    break

        if not is_contained:
            return

        self._voc.append(
            {
                "index": index,
                "grade": grade,
                "word": word.strip(),
                "answer": answer.strip(),
            }
        )

    def _print_question(
        self,
        descr,
    ):
        print(
            "Word #{index}:\n{word} [{grade}]".format(
                index=descr["index"],
                word=descr["word"],
                grade=descr["grade"],
            )
        )

    def _handle_input(
        self,
        descr,
    ):
        input()

    def _display_answer(
        self,
        descr,
    ):
        print("Answer:\n{answer}\n".format(answer=descr["answer"]))
        print("**************************************************\n")

    def train(
        self,
        grades=None,
    ):
        if self._voc is None:
            print("Vocabulary not initialized.")
            return

        count = len(self._voc)

        if count <= 0:
            print("Nothing to see here...")
            return

        print(
            "{count} word(s) to review!".format(
                count=count,
            )
        )

        while count > 0:
            descr = self._voc.pop(randrange(count))
            count -= 1

            self._print_question(descr)
            self._handle_input(descr)
            self._display_answer(descr)

        print("You did it!")
