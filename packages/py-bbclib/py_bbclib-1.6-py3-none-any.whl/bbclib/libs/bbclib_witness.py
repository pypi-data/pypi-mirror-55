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
See the License for the  specific language governing permissions and
limitations under the License.
"""
import os
import sys

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(current_dir, "../.."))

from bbclib import id_length_conf
from bbclib.libs import bbclib_binary


class BBcWitness:
    """Witness part in a transaction"""
    def __init__(self, id_length=None, version=2):
        self.idlen_conf = id_length_conf.copy()
        self.version = version
        if id_length is not None:
            if isinstance(id_length, int):
                for k in self.idlen_conf.keys():
                    self.idlen_conf[k] = id_length
            elif isinstance(id_length, dict):
                for k in id_length.keys():
                    self.idlen_conf[k] = id_length[k]
        self.transaction = None
        self.user_ids = list()
        self.sig_indices = list()

    def __str__(self):
        ret = "Witness:\n"
        for i in range(len(self.sig_indices)):
            ret += " [%d]\n" % i
            if self.user_ids[i] is not None:
                ret += "  user_id: %s\n" % bbclib_binary.str_binary(self.user_ids[i])
                ret += "  sig_index: %d\n" % self.sig_indices[i]
            else:
                ret += "  None (invalid)\n"
        return ret

    def add_witness(self, user_id):
        """Register user_id in the list"""
        if user_id not in self.user_ids:
            self.user_ids.append(user_id[:self.idlen_conf["user_id"]])
            self.sig_indices.append(self.transaction.get_sig_index(user_id[:self.idlen_conf["user_id"]]))

    def add_signature(self, user_id=None, signature=None):
        """Add signature in the reserved space for the user_id that was registered before

        Args:
            user_id (bytes): user_id of the signature owner
            signature (BBcSignature): signature
        """
        self.transaction.add_signature_object(user_id=user_id[:self.idlen_conf["user_id"]], signature=signature)

    def pack(self):
        """Pack this object

        Returns:
            bytes: packed binary data
        """
        dat = bytearray(bbclib_binary.to_2byte(len(self.sig_indices)))
        for i in range(len(self.sig_indices)):
            dat.extend(bbclib_binary.to_bigint(self.user_ids[i], size=self.idlen_conf["user_id"]))
            dat.extend(bbclib_binary.to_2byte(self.sig_indices[i]))
        return bytes(dat)

    def unpack(self, data):
        """Unpack into this object

        Args:
            data (bytes): packed binary data
        Returns:
            bool: True if successful
        """
        ptr = 0
        data_size = len(data)
        try:
            ptr, signum = bbclib_binary.get_n_byte_int(ptr, 2, data)
            self.user_ids = list()
            self.sig_indices = list()
            for i in range(signum):
                ptr, uid = bbclib_binary.get_bigint(ptr, data)
                self.idlen_conf["user_id"] = len(uid)
                self.user_ids.append(uid)
                ptr, idx = bbclib_binary.get_n_byte_int(ptr, 2, data)
                self.sig_indices.append(idx)
                if ptr > data_size:
                    return False
                self.transaction.set_sig_index(uid[:self.idlen_conf["transaction_id"]], idx)
        except:
            return False
        return True
