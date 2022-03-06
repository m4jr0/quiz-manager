#!/usr/bin/env python3

import argparse
import pathlib
import sys
import traceback

import quizmanager.gsheetquizmanager as gsheetquiz
import quizmanager.csvquizmanager as csvquiz
import configuration.settings as conf


is_debug = False


def file_path(path):
    if pathlib.Path(path).is_file():
        return path

    else:
        raise FileNotFoundError(path)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--filter",
        "-f",
        nargs="+",
        default=None,
        dest="raw_filters",
        help="argument(s) to provide to filter specific questions",
    )

    parser.add_argument(
        "--indexes",
        "-i",
        nargs="+",
        default=None,
        dest="raw_indexes",
        help="index(es) to provide to filter specific questions",
    )

    parser.add_argument(
        "--local",
        "-l",
        type=file_path,
        dest="csv_path",
        help='CSV file path. If provided, the program will be in a "local mode"',
    )

    parser.add_argument(
        "--document",
        "-d",
        type=str,
        dest="spreadsheet_descr_key",
        help="spreadsheet key in the settings file provided",
    )

    parser.add_argument(
        "--token",
        "-t",
        type=file_path,
        dest="token_path",
        help="token file path. If not given, a default token.json file in the script's folder will be read",
    )

    parser.add_argument(
        "--settings",
        "-s",
        type=file_path,
        dest="settings_path",
        help="settings file path. If not given, a default settings.json file in the script's folder will be read",
    )

    parser.add_argument(
        "--reversed",
        "-r",
        default=False,
        action="store_true",
        dest="is_reversed",
        help="whether to enable the reverse mode or not. If enabled, the answers will be displayed as questions, and questions as answers",
    )

    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        dest="is_debug",
        help="whether to enable the debug mode or not",
    )

    try:
        args = parser.parse_args()

    except FileNotFoundError as error:
        raise Exception(f"File not found: {error}")

        return

    global is_debug
    is_debug = args.is_debug

    if args.csv_path is not None:
        quiz_manager = csvquiz.CSVQuizManager(
            args.csv_path,
            args.is_reversed,
        )

        quiz_manager.initialize(args.raw_filters, args.raw_indexes)
        quiz_manager.do_quiz()
        return

    file_dir = pathlib.Path(__file__).parent
    token_path = args.token_path

    if token_path is None:
        token_path = file_dir / "token.json"

    settings_path = args.settings_path

    if settings_path is None:
        settings_path = file_dir / "settings.json"

    if args.spreadsheet_descr_key is None:
        print("Please provide a spreadsheet description key")
        return

    settings = conf.Settings(settings_path)
    settings.initialize()

    spreadsheet_descr = settings.get(args.spreadsheet_descr_key)

    if spreadsheet_descr is None:
        print("Please provide spreadsheet description in the settings file.")
        return

    spreadsheet_id = spreadsheet_descr["spreadsheet_id"]
    sheet = spreadsheet_descr["sheet"]
    range = spreadsheet_descr["range"]

    quiz_manager = gsheetquiz.GSheetQuizManager(
        token_path,
        spreadsheet_id,
        sheet,
        range,
        args.is_reversed,
    )

    quiz_manager.initialize(args.raw_filters, args.raw_indexes)
    quiz_manager.do_quiz()


if __name__ == "__main__":
    error_code = 0

    try:
        main()

    except KeyboardInterrupt:
        pass

    except Exception as error:
        if is_debug:
            print(traceback.format_exc())

        else:
            print(f"An error occurred: {error}. Aborting.")

        error_code = 1

    print("")
    sys.exit(error_code)
