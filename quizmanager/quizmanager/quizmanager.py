import abc

from random import randrange

from misc.interval import Interval


class AsbtractQuizManager(metaclass=abc.ABCMeta):
    GRADE_ALL = "All"
    GRADE_SERF = "Serf"
    GRADE_KNIGHT = "Knight"
    GRADE_WIZARD = "Wizard"
    GRADE_GOD = "God"

    GRADES = [
        GRADE_SERF,
        GRADE_KNIGHT,
        GRADE_WIZARD,
        GRADE_GOD,
    ]

    GRADES_LOWERCASE = []

    _quiz = None
    _is_reversed = False

    def __repr__(self):
        return "AsbtractQuizManager[len(_quiz): {quiz_len}, _is_reversed: {is_reversed}]".format(
            quiz_len=len(self._quiz) if self._quiz is not None else 0,
            is_reversed=self._is_reversed,
        )

    def __str__(self):
        return "AsbtractQuizManager[{question_count} question(s){reverse_label}]".format(
            question_count=len(self._quiz) if self._quiz is not None else 0,
            reverse_label="" if not is_reversed else " (reversed)",
        )

    def __init__(
        self,
        is_reversed=False,
    ):
        self._is_reversed = is_reversed

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

            elif grade not in cls.GRADES_LOWERCASE:
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
    def _build_quiz(
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
        for grade in self.GRADES:
            self.GRADES_LOWERCASE.append(grade.lower())

        grades = self.__get_grades(raw_grades)
        indexes = self.__get_indexes(raw_indexes)
        self._build_quiz(
            grades,
            indexes,
        )

    def reset(self):
        self._quiz = []

    def _handle_question(
        self,
        grades,
        indexes,
        index,
        grade,
        question,
        answer,
        notes,
    ):
        if not question or not answer:
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

        self._quiz.append(
            {
                "index": index,
                "grade": grade,
                "question": question.strip(),
                "answer": answer.strip(),
                "notes": notes.strip(),
            }
        )

    def _display_question(
        self,
        descr,
    ):
        print(
            "Question #{index} [{grade}]:\n{question}".format(
                index=descr["index"],
                grade=descr["grade"],
                question=self._get_question(descr),
            )
        )

    def _get_question(
        self,
        descr,
    ):
        if self._is_reversed:
            return descr["answer"]

        return descr["question"]

    def _handle_input(
        self,
        descr,
    ):
        input()

    def _get_answer(
        self,
        descr,
    ):
        if self._is_reversed:
            return descr["question"]

        return descr["answer"]

    def _get_notes(
        self,
        descr,
    ):
        return descr["notes"]

    def _display_answer(
        self,
        descr,
    ):
        print(
            "Answer:\n{answer}\n".format(
                answer=self._get_answer(descr),
            )
        )

    def _display_notes(
        self,
        descr,
    ):
        print(
            "Note(s):\n{notes}\n".format(
                notes=self._get_notes(descr),
            )
        )

    def _display_separator(
        self,
        descr,
    ):
        print("**************************************************\n")

    def do_quiz(
        self,
        grades=None,
    ):
        if self._quiz is None:
            print("Quiz not initialized.")
            return

        count = len(self._quiz)

        if count <= 0:
            print("Nothing to see here...")
            return

        print(
            "{count} question(s) to review!".format(
                count=count,
            )
        )

        while count > 0:
            descr = self._quiz.pop(randrange(count))
            count -= 1

            self._display_question(descr)
            self._handle_input(descr)
            self._display_answer(descr)
            self._display_notes(descr)
            self._display_separator(descr)

        print("You did it!")