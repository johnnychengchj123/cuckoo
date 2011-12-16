#!/usr/bin/python
# Cuckoo Sandbox - Automated Malware Analysis
# Copyright (C) 2010-2011  Claudio "nex" Guarnieri (nex@cuckoobox.org)
# http://www.cuckoobox.org
#
# This file is part of Cuckoo.
#
# Cuckoo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cuckoo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.    

import os
import sys

from cuckoo.reporting.observers import BaseObserver

class Report(BaseObserver):
    """
    Generates a human readable Text report.
    """
    
    def __init__(self):
        self._report = ""
        self._results = None

    def _add_line(self):
        self._report += "================================================================================\n"

    def _gen_header(self):
        self._report += "                                       _                  \n"
        self._report += "                      ____ _   _  ____| |  _ ___   ___    \n"
        self._report += "                     / ___) | | |/ ___) |_/ ) _ \\ / _ \\ \n"
        self._report += "                    ( (___| |_| ( (___|  _ ( |_| | |_| |  \n"
        self._report += "                     \\____)____/ \\____)_| \_)___/ \\___/\n"
        self._report += "\n"
        self._report += "                              Analysis Report\n"
        self._report += "                            <----------------->\n"
        self._report += "                             www.cuckoobox.org\n"
        self._report += "\n"
        self._add_line()
        self._report += " Analysis of %s\n" % self._results["file"]["name"]
        self._report += " MD5 %s\n" % self._results["file"]["md5"]
        self._add_line()
        self._report += "\n"

    def _gen_menu(self):
        self._add_line()
        self._report += " Content Menu\n"
        self._add_line()
        self._report += "\n"

        self._report += "    1. General information\n"
        self._report += "    2. Dropped files\n"

        if self._results["dropped"] and len(self._results["dropped"]) > 0:
            counter = 1
            for dropped in self._results["dropped"]:
                self._report += ("        2.%d File: %s\n" 
                                 % (counter, dropped["name"]))
                counter += 1

        self._report += "    3. Network analysis\n"
        self._report += "        3.1 DNS requests\n"
        self._report += "        3.2 HTTP requests\n"
        self._report += "    4. Behavior analysis\n"

        counter = 1
        for process in self._results["behavior"]["processes"]:
            self._report += ("        4.%d Process: %s (%s)\n" 
                             % (counter, process["process_name"],
                                process["process_id"]))
            counter += 1

        self._report += "\n"

    def _gen_general_information(self):
        self._add_line()
        self._report += " 1. General information\n"
        self._add_line()
        self._report += "\n"

        self._report += ("This report has been generated by Cuckoo Sandbox %s.\n" 
                         % self._results["info"]["version"])
        self._report += ("The analysis started at: %s\n"
                         % self._results["info"]["started"])
        self._report += ("The analysis lasted: %s seconds\n"
                         % self._results["info"]["duration"])
        self._report += "\n"
        self._report += "File name: %s\n" % self._results["file"]["name"]
        self._report += "File size: %d bytes\n" % self._results["file"]["size"]
        self._report += "File type: %s\n" % self._results["file"]["type"]
        self._report += "CRC32:     %s\n" % self._results["file"]["crc32"]
        self._report += "MD5:       %s\n" % self._results["file"]["md5"]
        self._report += "SHA-1:     %s\n" % self._results["file"]["sha1"]
        self._report += "SHA-256:   %s\n" % self._results["file"]["sha256"]
        self._report += "SHA-512:   %s\n" % self._results["file"]["sha512"]
        self._report += "Ssdeep:    %s\n" % self._results["file"]["ssdeep"]

        self._report += "\n"

    def _gen_dropped(self):
        self._add_line()
        self._report += " 2. Dropped files\n"
        self._add_line()
        self._report += "\n"

        if len(self._results["dropped"]) > 0:
            counter = 1
            for dropped in self._results["dropped"]:
                self._report += "[2.%d] \"%s\":\n" % (counter, dropped["name"])
                self._report += "  File size: %s bytes\n" % dropped["size"]
                self._report += "  File type: %s\n" % dropped["type"]
                self._report += "  CRC32:     %s\n" % dropped["crc32"]
                self._report += "  MD5:       %s\n" % dropped["md5"]
                self._report += "  SHA-1:     %s\n" % dropped["sha1"]
                self._report += "  SHA-256:   %s\n" % dropped["sha256"]
                self._report += "  SHA-512:   %s\n" % dropped["sha512"]
                self._report += "  Ssdeep:    %s\n" % dropped["ssdeep"]
                self._report += "\n"

                counter += 1
        else:
            self._report += "Nothing to display.\n"

        self._report += "\n"

    def _gen_network(self):
        self._add_line()
        self._report += " 5. Network analysis\n"
        self._add_line()
        self._report += "\n"

        self._report += "[5.1] DNS Requests:\n"
        if self._results["network"] and \
           len(self._results["network"]["dns"]) > 0:
            for dns in self._results["network"]["dns"]:
                self._report += ("  Hostname: %s, IP: %s\n"
                                 % (dns["hostname"], dns["ip"]))
        else:
            self._report += "  Nothing to display.\n"

        self._report += "\n"

        self._report += "[5.2] HTTP Requests:\n"
        if self._results["network"] and \
           len(self._results["network"]["http"]) > 0:
            for http in self._results["network"]["http"]:
                self._report += ("  Host: %s, Port: %s, URI: %s\n"
                                 % (http["host"], http["port"], http["uri"]))
        else:
            self._report += "  Nothing to display.\n"

        self._report += "\n"

    def _gen_processes(self):
        self._add_line()
        self._report += " 4. Behavior analysis\n"
        self._add_line()
        self._report += "\n"

        if len(self._results["behavior"]["processes"]) > 0:
            counter = 1
            for process in self._results["behavior"]["processes"]:
                self._report += ("[4.%d] Process: %s (%s):\n"
                                 % (counter,
                                    process["process_name"],
                                    process["process_id"]))

                for call in process["calls"]:
                    self._report += ("  (%s) Function: %s, Status: %s, Return: %s\n"
                                     % (call["timestamp"],
                                        call["api"],
                                        call["status"],
                                        call["return"]))

                    for argument in call["arguments"]:
                        self._report += ("      Argument: %s, Value: %s\n"
                                         % (argument["name"],
                                            argument["value"]))

                self._report += "\n"
                counter += 1
        else:
            self._report += "Nothing to display."

        self._report += "\n"

    def _gen_report(self):
        self._gen_header()
        self._gen_menu()
        self._gen_general_information()
        self._gen_dropped()
        self._gen_network()
        self._gen_processes()
    
    def update(self, results):
        report_path = os.path.join(sys.argv[1], "reports")
        if not os.path.exists(report_path):
            os.mkdir(report_path)

        self._results = results
        self._gen_report()

        report = open(os.path.join(report_path, "report.txt"), "w")
        report.write(self._report)
        report.close()
