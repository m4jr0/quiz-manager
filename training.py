#!/usr/bin/env python3

import argparse
import sys

from vocbuilder.vocbuilder import VocBuilder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", "-f", nargs="+", default=None)
    parser.add_argument("--indexes", "-i", nargs="+", default=None)
    args = parser.parse_args()

    builder = VocBuilder()
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
