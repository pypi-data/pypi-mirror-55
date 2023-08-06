"""
licenseit

Usage:
    licenseit new [--license=license|--author=name|--year=year|-l=license|-a=name|-y=year]
    licenseit init [--license=license|--author=name|--year=year|-l=license|-a=name|-y=year]
    licenseit limitations
    licenseit -h | --help
    licenseit -v | --version

Options:

    new             Creates a LICENSE file.
    init            Creates a LICENSE file.
    limitations     Shows limitations of a given license.
    -h --help       Shows possible commands.
    -v --version    Shows current version of the package.

Help:
    For suggestions/problems and etc. visit the github reposityory https://github.com/monzita/licenseit
"""
import datetime as dt

from docopt import docopt
from licenseit.commands import License

VERSION = "0.1.1"

import sys


def main():
    global VERSION

    fix_name(sys.argv)

    if invalid_options(sys.argv[2:]):
        docopt(__doc__, version=VERSION)
        return

    index = (
        sys.argv.index("new")
        if "new" in sys.argv
        else sys.argv.index("init")
        if "init" in sys.argv
        else -1
    )
    suboptions = sys.argv[index + 1 :] if index > 0 else {}
    license, author, year = [None] * 3
    if suboptions:
        sys.argv = list(filter(lambda v: v not in suboptions, sys.argv))
        suboptions = {
            option[: option.index("=")]: option[option.index("=") + 1 :].replace(
                "'", ""
            )
            for option in suboptions
        }
        license = (
            suboptions.get("--license", str()) or suboptions.get("-l", str()).lower()
        )
        author = suboptions.get("--author", str()) or suboptions.get("-a", str())
        year = (
            suboptions.get("--year", 0)
            or suboptions.get("-y", 0)
            or dt.datetime.today().year
        )

    options = docopt(__doc__, version=VERSION)

    new = options.get("new", 0) or options.get("init", 0)

    if new:
        if not license:
            license, author, year = License.choose()
        License.create(license, author, year)
    elif options["-v"]:
        print(VERSION)
    else:
        pass


def invalid_options(args):
    return any(
        filter(
            lambda op: op.split("=")[0]
            not in ["-l", "--license", "-y", "--year", "-a", "--author"],
            args,
        )
    )


def fix_name(args):
    index = [
        index
        for index, option in enumerate(args)
        if "-a" in option or "--author" in option
    ]

    if index:
        index = index[0]
        next_option_index = [
            i
            for i, option in enumerate(args[index + 1 :])
            if any(filter(lambda op: op in option, ["-l", "--license", "-y", "--year"]))
        ]

        if next_option_index:
            next_option_index = next_option_index[0]
            next_option_index += index + 1
        else:
            next_option_index = len(args)

        args[index:next_option_index] = [" ".join(args[index:next_option_index])]
