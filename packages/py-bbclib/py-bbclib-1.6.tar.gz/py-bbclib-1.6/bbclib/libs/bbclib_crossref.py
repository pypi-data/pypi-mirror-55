# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 beyond-blockchain.org.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(current_dir, "../.."))

from bbclib.libs import bbclib_binary
from bbclib import id_length_conf


class BBcCrossRef:
    """CrossRef part in a transaction"""
    def __init__(self, domain_id=None, transaction_id=None, unpack=None):
        self.idlen_conf = id_length_conf.copy()
        self.domain_id = domain_id
        self.transaction_id = transaction_id
        if unpack is not None:
            self.unpack(unpack)

    def __str__(self):
        ret  = "Cross_Ref:\n"
        ret += "  domain_id: %s\n" % bbclib_binary.str_binary(self.domain_id)
        ret += "  transaction_id: %s\n" % bbclib_binary.str_binary(self.transaction_id)
        return ret

    def pack(self):
        """Pack this object

        Returns:
            bytes: packed binary data
        """
        dat = bytearray(bbclib_binary.to_bigint(self.domain_id))
        dat.extend(bbclib_binary.to_bigint(self.transaction_id, self.idlen_conf["transaction_id"]))
        return bytes(dat)

    def unpack(self, data):
        """Unpack into this object

        Args:
            data (bytes): packed binary data
        Returns:
            bool: True if successful
        """
        ptr = 0
        try:
            ptr, self.domain_id = bbclib_binary.get_bigint(ptr, data)
            ptr, self.transaction_id = bbclib_binary.get_bigint(ptr, data)
            self.idlen_conf["transaction_id"] = len(self.transaction_id)
        except:
            return False
        return True
