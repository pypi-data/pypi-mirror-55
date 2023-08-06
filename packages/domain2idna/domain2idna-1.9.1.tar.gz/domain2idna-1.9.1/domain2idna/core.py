#!/usr/bin/env python

"""
domain2idna - The tool to convert a domain or a file with a list
of domain to the famous IDNA format.

This module is the core of the module/library. It contains the brain of the program.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Contributors:
    Let's contribute to domains2idna!!

Project link:
    https://github.com/PyFunceble/domain2idna

Project documentation:
    http://domain2idna.readthedocs.io

License:
    MIT License

    Copyright (c) 2018-2019 Nissar Chababy
    Copyright (c) 2019 PyFunceble

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: disable=bad-continuation


class Core:  # pylint: disable=too-few-public-methods
    """
    Brain of the program

    :param domains:
        The domain or domains to convert.
    :type domains: str, list
    """

    def __init__(self, domains):
        self.domains = domains
        self.to_ignore = [
            "0.0.0.0",
            "localhost",
            "127.0.0.1",
            "localdomain",
            "local",
            "broadcasthost",
            "allhosts",
            "allnodes",
            "allrouters",
            "localnet",
            "loopback",
            "mcastprefix",
        ]

    @classmethod
    def _convert_it_to_idna(cls, string):
        """
        Converts the given string to IDNA.

        :param str string:
            The string to convert.

        :rtype: str
        """

        return string.encode("idna").decode("utf-8")

    def to_idna(self):
        """
        Converts a domain from the given list.

        :return:
            str:
                if a single domain is given.
            list:
                If a list of domain is given.
        :rtype: str, list
        """

        if isinstance(self.domains, list):  # pylint: disable=too-many-nested-blocks
            result = []

            for domain in self.domains:
                if (
                    domain
                    and domain not in self.to_ignore
                    and domain.strip()
                    and not domain.startswith("#")  # pylint: disable=line-too-long
                ):
                    splited_domain = domain.split()
                    local_result = []

                    for element in splited_domain:
                        if element not in self.to_ignore:
                            try:
                                local_result.append(self._convert_it_to_idna(element))
                            except UnicodeError:  # pragma: no cover
                                local_result.append(element)
                        else:
                            local_result.append(element)

                    result.append(" ".join(local_result))
                else:
                    result.append(domain)

            return result

        domains = self.domains.strip().split()

        if len(domains) > 1:
            return " ".join(Core(domains).to_idna())

        try:
            return self._convert_it_to_idna(self.domains)

        except UnicodeError:  # pragma: no cover
            return self.domains
