import pkg_resources
import os

ENCODING = "utf-8"


def get_license(license, author, year):
    global ENCODING

    year = bytes(str(year), ENCODING)
    author = bytes(author, ENCODING)

    recourse_package = __name__
    resource_path = (os.sep).join(("content", "{}.txt".format(license)))

    license = pkg_resources.resource_string(recourse_package, resource_path)
    license = license.replace(b"<YEAR>", year)

    if author:
        license = license.replace(b"<COPYRIGHT HOLDERS>", author)

    return license.decode(ENCODING)
