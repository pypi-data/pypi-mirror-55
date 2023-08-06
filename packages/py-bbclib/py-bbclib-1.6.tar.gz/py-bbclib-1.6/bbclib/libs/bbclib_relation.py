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
import sys
import os
import traceback

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(current_dir, "../.."))
from bbclib.libs import bbclib_binary
from bbclib.libs.bbclib_pointer import BBcPointer
from bbclib.libs.bbclib_asset import BBcAsset
from bbclib.libs.bbclib_asset_raw import BBcAssetRaw
from bbclib.libs.bbclib_asset_hash import BBcAssetHash
from bbclib import id_length_conf


class BBcRelation:
    """Relation part in a transaction"""
    def __init__(self, asset_group_id=None, id_length=None, version=1):
        self.version = version
        self.idlen_conf = id_length_conf.copy()
        if id_length is not None:
            if isinstance(id_length, int):
                for k in self.idlen_conf.keys():
                    self.idlen_conf[k] = id_length
            elif isinstance(id_length, dict):
                for k in id_length.keys():
                    self.idlen_conf[k] = id_length[k]
        if asset_group_id is not None:
            self.asset_group_id = asset_group_id[:self.idlen_conf["asset_group_id"]]
        else:
            self.asset_group_id = None
        self.pointers = list()
        self.asset = None
        self.asset_raw = None
        self.asset_hash = None

    def __str__(self):
        ret =  "  asset_group_id: %s\n" % bbclib_binary.str_binary(self.asset_group_id)
        if len(self.pointers) > 0:
            ret += "  Pointers[]: %d\n" % len(self.pointers)
            for i, pt in enumerate(self.pointers):
                ret += "   [%d]\n" % i
                ret += str(pt)
        if self.asset is not None:
            ret += str(self.asset)
        if self.asset_raw is not None:
            ret += str(self.asset_raw)
        if self.asset_hash is not None:
            ret += str(self.asset_hash)
        return ret

    def add(self, asset_group_id=None, asset=None, asset_raw=None, asset_hash=None, pointer=None):
        """Add parts"""
        if asset_group_id is not None:
            self.asset_group_id = asset_group_id[:self.idlen_conf["asset_group_id"]]
        if pointer is not None:
            if isinstance(pointer, list):
                self.pointers.extend(pointer)
            else:
                self.pointers.append(pointer)
        if asset is not None:
            self.asset = asset
        if asset_raw is not None:
            self.asset_raw = asset_raw
        if asset_hash is not None:
            self.asset_hash = asset_hash
        return True

    def set_asset_group(self, asset_group_id):
        """Set asset_group_id in the BBcRelation object

        Args:
            asset_group_id (byte): asset_group_id
        Returns:
            BBcRelation: this object
        """
        if asset_group_id is not None:
            self.asset_group_id = asset_group_id[:self.idlen_conf["asset_group_id"]]
        return self

    def create_asset(self, user_id, asset_body=None, asset_file=None):
        """Create BBcAsset object and set it to self.asset in the BBcRelation object

        Args:
            user_id (byte): user_id to set in BBcAsset object
            asset_body (*): asset_body to set in BBcAsset object
            asset_file (byte): asset file to set in BBcAsset object
        Returns:
            BBcRelation: this object
        """
        self.asset = BBcAsset(user_id=user_id, asset_file=asset_file, asset_body=asset_body,
                              id_length=self.idlen_conf, version=self.version)
        return self

    def create_asset_raw(self, asset_id, asset_body=None):
        """Create BBcAssetRaw object and set it to self.asset in the BBcRelation object

        Args:
            asset_id (byte): asset_id to set in BBcAssetRaw object
            asset_body (*): asset_body to set in BBcAssetRaw object
        Returns:
            BBcRelation: this object
        """
        self.asset_raw = BBcAssetRaw(asset_id=asset_id, asset_body=asset_body,
                                     id_length=self.idlen_conf, version=self.version)
        return self

    def create_asset_hash(self, asset_ids):
        """Create BBcAssetHash object and set it to self.asset in the BBcRelation object

        Args:
            asset_ids (list(byte)): list of asset_ids to set in BBcAssetRaw object
        Returns:
            BBcRelation: this object
        """
        self.asset_hash = BBcAssetHash(asset_ids=asset_ids, id_length=self.idlen_conf, version=self.version)
        return self

    def create_pointer(self, transaction_id=None, asset_id=None):
        """Create BBcPointer object and set it to self.asset in the BBcRelation object

        Args:
            transaction_id (byte): transaction_id
            asset_id (byte): asset_id
        Returns:
            BBcRelation: this object
        """
        pointer = BBcPointer(transaction_id=transaction_id, asset_id=asset_id, id_length=self.idlen_conf, version=self.version)
        self.pointers.append(pointer)
        return self

    def pack(self):
        """Pack this object

        Returns:
            bytes: packed binary data
        """
        if self.asset_group_id is None:
            raise Exception("need asset_group_id in BBcRelation")
        dat = bytearray(bbclib_binary.to_bigint(self.asset_group_id, size=self.idlen_conf["asset_group_id"]))
        dat.extend(bbclib_binary.to_2byte(len(self.pointers)))
        for i in range(len(self.pointers)):
            pt = self.pointers[i].pack()
            dat.extend(bbclib_binary.to_2byte(len(pt)))
            dat.extend(pt)
        if self.asset is not None:
            ast = self.asset.pack()
            dat.extend(bbclib_binary.to_4byte(len(ast)))
            dat.extend(ast)
        else:
            dat.extend(bbclib_binary.to_4byte(0))
        if self.version >= 2:
            if self.asset_raw is not None:
                ast = self.asset_raw.pack()
                dat.extend(bbclib_binary.to_4byte(len(ast)))
                dat.extend(ast)
            else:
                dat.extend(bbclib_binary.to_4byte(0))
            if self.asset_hash is not None:
                ast = self.asset_hash.pack()
                dat.extend(bbclib_binary.to_4byte(len(ast)))
                dat.extend(ast)
            else:
                dat.extend(bbclib_binary.to_4byte(0))
        return bytes(dat)

    def unpack(self, data, version=2):
        """Unpack data into transaction object

        Args:
            data (bytes): packed binary data
            version (int): version of the data format
        Returns:
            bool: True if successful
        """
        ptr = 0
        self.version = version
        data_size = len(data)
        try:
            ptr, self.asset_group_id = bbclib_binary.get_bigint(ptr, data)
            self.idlen_conf["asset_group_id"]= len(self.asset_group_id)
            ptr, pt_num = bbclib_binary.get_n_byte_int(ptr, 2, data)
            self.pointers = list()
            for i in range(pt_num):
                ptr, size = bbclib_binary.get_n_byte_int(ptr, 2, data)
                ptr, ptdata = bbclib_binary.get_n_bytes(ptr, size, data)
                if ptr >= data_size:
                    return False
                pt = BBcPointer()
                if not pt.unpack(ptdata):
                    return False
                self.pointers.append(pt)
            self.asset = None
            ptr, astsize = bbclib_binary.get_n_byte_int(ptr, 4, data)
            if astsize > 0:
                self.asset = BBcAsset()
                ptr, astdata = bbclib_binary.get_n_bytes(ptr, astsize, data)
                if not self.asset.unpack(astdata):
                    return False

            if version >= 2:
                self.asset_raw = None
                ptr, astsize = bbclib_binary.get_n_byte_int(ptr, 4, data)
                if astsize > 0:
                    self.asset_raw = BBcAssetRaw()
                    ptr, astdata = bbclib_binary.get_n_bytes(ptr, astsize, data)
                    if not self.asset_raw.unpack(astdata):
                        return False
                self.asset_hash = None
                ptr, astsize = bbclib_binary.get_n_byte_int(ptr, 4, data)
                if astsize > 0:
                    self.asset_hash = BBcAssetHash()
                    ptr, astdata = bbclib_binary.get_n_bytes(ptr, astsize, data)
                    if not self.asset_hash.unpack(astdata):
                        return False

        except:
            return False
        return True
