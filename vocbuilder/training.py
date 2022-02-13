#!/usr/bin/env python3

import argparse
import pathlib
import sys

import builder.gsheetvocbuilder as voc
import configuration.settings as conf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", "-f", nargs="+", default=None)
    parser.add_argument("--indexes", "-i", nargs="+", default=None)
    args = parser.parse_args()

    file_dir = pathlib.Path(__file__).parent
    settings = conf.Settings(file_dir.parent / "settings.json")
    settings.initialize()

    token_path = settings.get("gdrive")["token_path"]
    spreadsheet_id = settings.get("english")["spreadsheet_id"]
    sheet = settings.get("english")["sheet"]
    range = settings.get("english")["range"]

    builder = voc.GSheetVocBuilder(
        file_dir / token_path,
        spreadsheet_id,
        sheet,
        range,
    )

    builder.initialize(args.filter, args.indexes)
    builder.train()


if __name__ == "__main__":
    error_code = 0

    try:
        main()

    except KeyboardInterrupt:
        pass

    except Exception as error:
        print(
            "An error occurred: {error}. Aborting.".format(
                error=error,
            )
        )

        error_code = 1

    print("")
    sys.exit(error_code)
