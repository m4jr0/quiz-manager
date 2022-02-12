#!/usr/bin/env python3

import argparse
import pathlib
import sys

import builder.localvocbuilder as voc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", "-f", nargs="+", default=None)
    parser.add_argument("--indexes", "-i", nargs="+", default=None)
    args = parser.parse_args()

    builder = voc.LocalVocBuilder(
        pathlib.Path(__file__).parent.parent / "training.csv"
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
