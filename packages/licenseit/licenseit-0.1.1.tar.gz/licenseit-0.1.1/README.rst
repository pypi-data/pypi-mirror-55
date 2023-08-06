LicenseIT |img|
===============

.. |img| image:: https://s14.postimg.cc/3zf2q1fpd/if_new-24_103173_3.png


1. **Install**

>>> pip install licenseit

2. **Options**

>>> licenseit init | new [--license=license|--author=name|--year=year|-l=license|-a=name|-y=year]
>>> license -h | --help
>>> license -v | --version

3. **Usage**

>>> licenseit init | new
>>> Choose a license:
        1. Academic Free License v3.0
        2. Adaptive public license
        3. Apache license-2.0
        4. Artistic License 2.0
        5. BSD-2-Clause-Patent
        6. BSD-2-Clause
        7. BSD-3-Clause
        8. Boost Software License 1.0 (BSL-1.0)
        9. Common Development and Distribution License
        10. Do What The F-ck You Want To Public License
        11. Educational Community License
        12. Eclipse Public License - v 2.0
        13. GNU Affero General Public License v3.0
        14. GNU GENERAL PUBLIC LICENSE 2.0
        15. GNU GENERAL PUBLIC LICENSE 3.0
        16. IPA Font License Agreement v1.0
        17. ISC
        18. LaTeX Project Public License, Version 1.3c (LPPL-1.3c)
        19. GNU LIBRARY GENERAL PUBLIC LICENSE 2.0
        20. GNU Lesser General Public License 2.0
        21. GNU Lesser General Public License v3.0
        22. MIT
        23. Microsoft Public License
        24. Mozilla Public License, version 2.0
        25. NASA OPEN SOURCE AGREEMENT VERSION 1.3
        26. SIL OPEN FONT LICENSE
        27. OSET PUBLIC LICENSE 2.1
        28. The Open Software License 3.0 (OSL-3.0)
        29. The PostgreSQL Licence (PostgreSQL)
        30. The Unlicense
        31. The zlib-libpng License (Zlib)
        32. Upstream Compatibility License v. 1.0 (UCL-1.0)
License (default MIT):
>>> Author:
>>> Year:

OR

>>> licenseit (init | new) -l=mit -a='Your name / company' -y=year (default is current year)
>>> licenseit (init | new) -license=mit -author='Your name / company' -year=year (default is current year)

4. **Licenses**

====================================================== ================
License                                                License keyword
====================================================== ================
Academic Free License v3.0                  	       ``afl-3.0``
Apache license 2.0                                     ``apache-2.0``
Adaptive public license                                ``apl``
Artistic License 2.0                                   ``artistic-2.0``
BSD-2-Clause-Patent                                    ``bsd-2``
BSD-2-Clause                                           ``bsd-2-cl``
BSD-3-Clause                                           ``bsd-3-cl``
Boost Software License 1.0 (BSL-1.0)                   ``bsl-1.0``
Common Development and Distribution License            ``cddl``
Do What The F*ck You Want To Public License 	       ``wtfpl``
Educational Community License                          ``ecl``
Eclipse Public License - v 2.0                         ``epl-2.0``
GNU Affero General Public License v3.0                 ``agpl-3.0``
GNU GENERAL PUBLIC LICENSE 2.0                         ``gnu-2.0``
GNU GENERAL PUBLIC LICENSE 3.0                         ``gnu-3.0``
IPA Font License Agreement v1.0                        ``ipafla-1.0``
ISC                                                    ``isc``
LaTeX Project Public License, Version 1.3c (LPPL-1.3c) ``lppl-1.3c``
GNU LIBRARY GENERAL PUBLIC LICENSE 2.0                 ``lgnu-2.0``
GNU Lesser General Public License 2.0                  ``lgpl-2.0``
GNU Affero General Public License v3.0                 ``agpl-3.0``
Microsoft Public License                               ``ms-pl``
MIT                                                    ``mit``
Mozilla Public License, version 2.0                    ``mpl-2.0``
NASA OPEN SOURCE AGREEMENT VERSION 1.3                 ``nosav-1.3``
SIL OPEN FONT LICENSE                                  ``ofl-1.1``
OSET PUBLIC LICENSE 2.1                                ``opl-2.1``
The Open Software License 3.0 (OSL-3.0)                ``osl-3.0``
The PostgreSQL Licence (PostgreSQL)                    ``postgresql``
The Unlicense                                          ``unlicense``
The zlib/libpng License (Zlib)                         ``zlib``
Upstream Compatibility License v. 1.0 (UCL-1.0)        ``ucl-1.0``
====================================================== ================

Check about limitations of all licenses at `choosealicense <https://choosealicense.com>`_

5. **Updates**

``11/11/2019`` 

1. Added new licenses.

``Academic Free License v3.0``, ``Boost Software License 1.0``, ``Do What The F-ck You Want To Public License``, ``LaTeX Project Public License, Version 1.3c (LPPL-1.3c)``, ``The Open Software License 3.0 (OSL-3.0)  ``, ``The PostgreSQL Licence (PostgreSQL)``, ``The Unlicense``, ``The zlib/libpng License (Zlib)``, ``GNU Affero General Public License v3.0``, ``GNU Lesser General Public License v3.0``, ``Microsoft Public License``

2. Added new options for generating a license.

``--license=license|-l=license`` Adds a license, where ``license`` is some of the keywords given in the table above.

``--author=name|-a=name`` Name of the author | organization.

``--year=year|-y=year`` By default is set to the current year, if not explicitly specified.

6. **Popular sites for licenses**

`OpenSourse <https://opensource.org/licenses>`_

`ChooseALicense <https://choosealicense.com>`_