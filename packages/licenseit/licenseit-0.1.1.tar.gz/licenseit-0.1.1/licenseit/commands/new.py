import datetime as dt

from ..licenses import get_license


class License(object):

    LICENSE = {
        "afl-3.0": "Academic Free License v3.0",
        "apl": "Adaptive public license",
        "apache-2.0": "Apache license-2.0",
        "artistic-2.0": "Artistic License 2.0",
        "bsd-2": "BSD-2-Clause-Patent",
        "bsd-2-cl": "BSD-2-Clause",
        "bsd-3-cl": "BSD-3-Clause",
        "bsl-1.0": "Boost Software License 1.0 (BSL-1.0)",
        "cddl": "Common Development and Distribution License",
        'wtfpl': "Do What The F-ck You Want To Public License",
        "ecl": "Educational Community License",
        "epl-2.0": "Eclipse Public License - v 2.0",
        "agpl-3.0": "GNU Affero General Public License v3.0",
        "gnu-2.0": "GNU GENERAL PUBLIC LICENSE 2.0",
        "gnu-3.0": "GNU GENERAL PUBLIC LICENSE 3.0",
        "ipafla-1.0": "IPA Font License Agreement v1.0",
        "isc": "ISC",
        "lppl-1.3c": "LaTeX Project Public License, Version 1.3c (LPPL-1.3c)",
        "lgnu-2.0": "GNU LIBRARY GENERAL PUBLIC LICENSE 2.0",
        "lgpl-2.0": "GNU Lesser General Public License 2.0",
        "lgpl-3.0": "GNU Lesser General Public License v3.0",
        "mit": "MIT",
        "ms-pl": "Microsoft Public License",
        "mpl-2.0": "Mozilla Public License, version 2.0",
        "nosav-1.3": "NASA OPEN SOURCE AGREEMENT VERSION 1.3",
        "ofl-1.1": "SIL OPEN FONT LICENSE",
        "opl-2.1": "OSET PUBLIC LICENSE 2.1",
        "osl-3.0": "The Open Software License 3.0 (OSL-3.0)",
        "postgresql": "The PostgreSQL Licence (PostgreSQL)",
        "unlicense": "The Unlicense",
        "zlib": "The zlib-libpng License (Zlib)",
        "ucl-1.0": "Upstream Compatibility License v. 1.0 (UCL-1.0)",
    }

    @classmethod
    def choose(cls):
        values = list(cls.LICENSE.values())
        choices = "\n".join(
            [
                "\t{}. {}".format(index + 1, license)
                for index, license in enumerate(values)
            ]
        )

        print("Licenses")
        print(choices)
        license_no = input("\nLicense (default MIT): ") or (values.index("MIT") + 1)
        while not int(license_no) in range(1, len(cls.LICENSE) + 1):
            license_no = input("\nLicense (default MIT): ") or (values.index("MIT") + 1)

        license = [
            key
            for key in cls.LICENSE.keys()
            if cls.LICENSE[key] == values[int(license_no) - 1]
        ][0]

        author = input("Author | Organization: ").strip()
        current_year = dt.datetime.now().year
        year = input("Year: (Default {}) ".format(current_year)) or str(current_year)
        while not cls._valid(str(year)):
            year = input("Year: (Default {}) ".format(current_year)) or str(
                current_year
            )
        return license, author, year

    @classmethod
    def _valid(cls, year):
        return len(year) == len([ch for ch in year if ch.isdigit()])

    @classmethod
    def create(cls, license, author, year):
        cls._init(license, author, year)

    @classmethod
    def _init(cls, license, author, year):

        license = cls.LICENSE.get(license, str())
        if not license:
            err = "Invalid choice for a license. Possible choices are: {}".format(
                ", ".join(cls.LICENSE.keys())
            )
            raise KeyError(err)

        license = get_license(license, author, year)

        with open("LICENSE", "w") as file:
            file.write(license)
