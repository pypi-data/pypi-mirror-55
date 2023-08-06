#  Copyright 2019 Andreas Krüger, DJ3EI
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# This finds the DXCC region for a given radio amateur call sign.

import os.path
import re
import sys
import urllib.request

class DxccUnknownException(Exception):
    """Exception to be raised if the DXCC cannot be determined."""
    pass

class DxccNode:
    def __init__(self):
        self.subnodes = {}
    
    def _subnode_for(self, char):
        subnode = self.subnodes.get(char)
        if subnode:
            return subnode
        else:
            subnode = DxccNode()
            self.subnodes[char] = subnode
            return subnode

    def book(self, call_prefix, name, continent, dxcc_number):
        if len(call_prefix) == 0:
            self.data = (name, continent, dxcc_number)
        else:
            subnode = self._subnode_for(call_prefix[0])
            subnode.book(call_prefix[1:], name, continent, dxcc_number)
    
    def data4(self, call):
        return self._data4(call, call)
            
    def _data4(self, call, calltail):
        if len(calltail) == 0:
            if hasattr(self, "data") and self.data:
                return self.data
            else:
                raise RuntimeError("Something weird happened for {}, shorter than expected, logic error.", call)
        else:
            p = calltail[0]
            subnode = self.subnodes.get(p)
            if subnode:
                return subnode._data4(call, calltail[1:])
            elif hasattr(self, "data") and self.data:
                return self.data
            else:
                raise DxccUnknownException("Incomplete data for {}, don't know the DXCC for that one.".format(call))
            
root_node = DxccNode()

def book(call_prefixes, name, continent, dxcc_number):
    if len(call_prefixes) == 0:
        raise RuntimeError("Internal: Prefix empty too short for {}.".format(name))
        
    if "/" in call_prefixes:
        if call_prefixes == "CE9/KC4":
            # book("CE9", name, continent, dxcc_number) # This is also Shetland islands.
            book("KC4", name, continent, dxcc_number)
            for n in ["0", "1", "2", "3", "5", "6", "7", "8", "9"]:
                book("KC" + n, "United States of America", "NA", 291)
        else:
            # print("WARNING: For now, ignoring {} for {}".format(call_prefixes, name), file=sys.stderr)
            pass
        return

    comma_i = call_prefixes.find(",")
    if 0 <= comma_i:
        if "T8," == call_prefixes:
            book("T8", name, continent, dxcc_number)
        else: 
            # DU-DZ,4D-4I or FT/J,E,TO or G,GX,M
            book(call_prefixes[0:comma_i], name, continent, dxcc_number)
            book(call_prefixes[comma_i + 1:], name, continent, dxcc_number)
        return

    if "_" in call_prefixes:
        if "4U_ITU" == call_prefixes or "4U_UN" == call_prefixes:
            tail = call_prefixes[3:]
            for c in range (ord("0"), ord("9") + 1):
                book("4U" + chr(c) + tail, name, continent, dxcc_number)
            for c in range (ord("A"), ord("Z") + 1):
                book("4U" + chr(c) + tail, name, continent, dxcc_number)
            return
        else:
            raise RuntimeError("Internal _: call_prefixes {}, name \"{}\", dxcc_number {}" \
                                   .format(call_prefixes, name, dxcc_number))


    minus_i = call_prefixes.find("-")
    if -1 < minus_i:
        if 1 < minus_i:
            call_prefs1 = call_prefixes[0:minus_i]
            call_prefs2 = call_prefixes[minus_i + 1:]
            if len(call_prefs1) == len(call_prefs2):
                # Could be either something like PA-PI or EA6-EH6
                prefix = call_prefs1[0:len(call_prefs1) - 1]
                if 0 == call_prefs2.find(prefix):
                    # Something like PA-PI
                    first_letter = call_prefs1[len(call_prefs1) - 1]
                    last_letter = call_prefs2[len(call_prefs2) - 1]
                    for letter_code in range(ord(first_letter), ord(last_letter) + 1):
                        call_prefix = prefix + chr(letter_code)
                        book(call_prefix, name, continent, dxcc_number)
                else:
                    # Something like EA6-EH6
                    if len(call_prefs1) == 3 and call_prefs1[0] == call_prefs2[0] and \
                        call_prefs1[2] == call_prefs2[2]:
                        first_letter = call_prefs1[1]
                        last_letter = call_prefs2[1]
                        for letter_code in range(ord(first_letter), ord(last_letter) + 1):
                            call_prefix = call_prefs1[0] + chr(letter_code) + call_prefs1[2]
                            book(call_prefix, name, continent, dxcc_number)
                    else:
                        raise RuntimeError("Internal: Do not understand {} in {}". \
                                           format(call_prefixes, name))
            elif call_prefixes in ["PP0-PY0F", "PP0-PY0S", "PP0-PY0T"]:
                return
            elif call_prefixes == "H6-7":
                book("H6", name, continent, dxcc_number)
                book("H7", name, continent, dxcc_number)
            elif call_prefixes == "UA-UI1-7":
                # This is guesswork:
                for nc in range(ord("1"), ord("7") + 1):
                    book("R" + chr(nc), name, continent, dxcc_number)
                    for lc in range(ord("A"), ord("Z") + 1):
                        book("R" + chr(lc) + chr(nc), name, continent, dxcc_number)
                    for lc in range(ord("A"), ord("I") + 1):
                        book("U" + chr(lc) + chr(nc), name, continent, dxcc_number)
            elif call_prefixes == "UA-UI8-0":
                # This is guesswork:
                for nc in ["8", "9", "0"]:
                    book("R" + nc, name, continent, dxcc_number)
                    for lc in range(ord("A"), ord("Z") + 1):
                        book("R" + chr(lc) + nc, name, continent, dxcc_number)
                    for lc in range(ord("A"), ord("I") + 1):
                        book("U" + chr(lc) + nc, name, continent, dxcc_number)
            else:
                raise RuntimeError("Internal -: call_prefixes {}, name \"{}\", dxcc_number {}" \
                                       .format(call_prefixes, name, dxcc_number))
            return
        else:
            raise RuntimeError("Internal -: call_prefixes {}, name \"{}\", dxcc_number {}" \
                                .format(call_prefixes, name, dxcc_number))
            return
    if "," in call_prefixes or "_" in call_prefixes or "-" in call_prefixes or "/" in call_prefixes:
        raise RuntimeError("Internal error: Unexpected here: {} for {}". \
                          format(call_prefixes, name))
    root_node.book(call_prefixes, name, continent, dxcc_number)

# Obtain file to local disk if not yet there:
dxcc_file = "dxcc.txt"
if not os.path.exists(dxcc_file):
    dxcc_uri = "http://www.arrl.org/files/file/DXCC/2019_Current_Deleted(3).txt"
    dxcc_file, headers = urllib.request.urlretrieve(dxcc_uri, filename="dxcc.txt")
    # print("{} {}".format(dxcc_file, headers))
    
reg2continent_dxcc_name = {}
with open(dxcc_file, mode="r", encoding="UTF-8") as dxcc_in:
    dxcc_txt = dxcc_in.read()
    parse_state = "SEARCHING_FOR_LIST"
    table_top = re.compile("[_ ]+")
    empty_line = re.compile(" *")
    data_line = re.compile(r"\s+([0-9A-Z,_\-\/]+)" \
                           r"(?:\#?\*?\(\d+\),?)*\#?\^?\*?\s+" \
                           r"(.*?)\s+" \
                           r"([A-Z]{2}(?:,[A-Z]{2})?)\s+" \
                           r"(\d{2}(?:[,\-]\d{2})?|\([A-Z]\))\s+" \
                           r"(\d{2}(?:[,\-]\d{2})?|\([A-Z]\))\s+0*(\d+?)(?:\s*?)")
    for line in dxcc_txt.splitlines():
        if parse_state == "SEARCHING_FOR_LIST":
            if table_top.fullmatch(line):
                parse_state = "TABLE"
        elif empty_line.fullmatch(line):
            break
        else:
            split = data_line.fullmatch(line)
            if not split:
                if "Spratly Is." in line:
                    pass # This is messy. Don't care about it.
                else:
                    raise RuntimeError("Ooops. Code is broken, cannot handle: \"{}\".".format(line))
            else:
                call_prefixes, name, continent, dxcc_number = split.group(1), split.group(2), split.group(3), int(split.group(6))
                # print((call_prefixes, name, continent, dxcc_number))
                book(call_prefixes, name, continent, dxcc_number)

# Stuff collected elsewhere:
book("CT8", "Azores", "EU", 149)  # http://www.425dxn.org/index.php?query=1484&op=wbull
book("CR2Y", "Azores", "EU", 149) # http://www.425dxn.org/index.php?query=1484&op=wbull
book("CR3", "Madeira Is.", "AF", 256)  # http://www.425dxn.org/index.php?query=1484&op=wbull
book("CT9", "Madeira Is.", "AF", 256)  # ? http://www.425dxn.org/index.php?query=1484&op=wbull
book("TM", "France", "EU", 227)   # ?
book("3Z", "Poland", "EU", 269)   # ?
book("4U1A", "United Nations Vienna", "EU", 117) # qrzcq.com
def data_for_call(call):
    return root_node.data4(call.upper())
