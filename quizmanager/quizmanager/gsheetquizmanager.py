import pathlib

import quizmanager.quizmanager as quiz
import handler.gdrivehandler as gdrive


class GSheetQuizManager(quiz.AsbtractQuizManager):
    __gdrive_handler = None
    __spreadsheet_id = None
    __sheet = None
    __range = None
    __grades_dict = {}

    YES_COMMANDS = [
        "y",
        "yea",
        "yeah",
        "yes",
        "sure",
        "why not",
        "please",
        "yes.avi",
    ]

    def __init__(
        self,
        token_path,
        spreadsheet_id,
        sheet,
        range,
        is_reversed=False,
    ):
        super().__init__(is_reversed)

        self.__gdrive_handler = gdrive.GDriveHandler(
            token_path,
            gdrive.GDriveHandler.SCOPE_SHEET,
        )

        self.__spreadsheet_id = spreadsheet_id
        self.__sheet = sheet
        self.__range = range

    def __repr__(self):
        return "GSheetQuizManager[len(_quiz): {quiz_len}, _is_reversed: {is_reversed}]".format(
            quiz_len=len(self._quiz) if self._quiz is not None else 0,
            is_reversed=self._is_reversed,
        )

    def __str__(self):
        return "GSheetQuizManager[{question_count} question(s){reverse_label}]".format(
            question_count=len(self._quiz) if self._quiz is not None else 0,
            reverse_label="" if not is_reversed else " (reversed)",
        )

    def initialize(
        self,
        raw_grades=None,
        raw_indexes=None,
    ):
        self.__gdrive_handler.initialize()
        super().initialize(raw_grades, raw_indexes)

        for grade in self.GRADES:
            grade_lower = grade.lower()
            self.__grades_dict[grade_lower] = grade
            first_char = grade_lower[0]

            if first_char in self.__grades_dict:
                print(
                    "Warning: duplicate entry for shortened grade {grade} ({first_char}). First grade was {first_grade}. Ignoring.".format(
                        grade=grade,
                        first_char=first_char,
                        first_grade=self.__grades_dict[first_char],
                    )
                )

                continue

            self.__grades_dict[first_char] = grade

    def _display_question(
        self,
        descr,
    ):
        super()._display_question(descr)

    def _handle_new_grade(
        self,
        descr,
    ):
        raw_new_grade = input("\n(Press ENTER to cancel) New grade: ")

        if not raw_new_grade:
            print("Aborting.\n")
            return

        if raw_new_grade not in self.__grades_dict:
            print(
                "\nInvalid grade: {grade}.".format(
                    grade=raw_new_grade,
                )
            )

            self._handle_new_grade(descr)
            return

        new_grade = self.__grades_dict[raw_new_grade]

        is_ok = self.__gdrive_handler.update_cell(
            self.__spreadsheet_id,
            self.__sheet,
            "B{cell_number}".format(
                cell_number=descr["index"] + 1,
            ),
            "RAW",
            {
                "values": [
                    [
                        new_grade,
                    ],
                ],
            },
        )

        if not is_ok:
            print("\nSomething wrong happened. Aborting.")
            return

        print(
            "\nNew grade set: {grade}.\n".format(
                grade=new_grade,
            )
        )

    def _display_answer(
        self,
        descr,
    ):
        super()._display_answer(descr)
        user_input = input("Set new grade? Answer: ")

        if not user_input:
            print("")
            return

        user_input = user_input.lower()

        if user_input not in self.YES_COMMANDS:
            print("")
            return

        self._handle_new_grade(descr)

    def _build_quiz(
        self,
        grades,
        indexes,
    ):
        self.reset()

        values = self.__gdrive_handler.fetch_values(
            self.__spreadsheet_id,
            self.__sheet,
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
            question = row[2]
            answer = row[3]

            self._handle_question(
                grades,
                indexes,
                index,
                grade,
                question,
                answer,
            )
