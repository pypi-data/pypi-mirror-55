"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Union

from ontology.exception.error_code import ErrorCode

from ontology.exception.exception import SDKException

from ontology.common.address import Address
from ontology.io.binary_writer import BinaryWriter
from ontology.core.transaction import Transaction, TxType
from ontology.vm.vm_type import VmType


class DeployTransaction(Transaction):
    def __init__(self, code: bytearray or str, vm_type: VmType, name: str = '', version: str = '', author: str = '',
                 email: str = '', description: str = '', gas_price: int = 0, gas_limit: int = 0,
                 payer: Union[str, bytes, Address, None] = b''):
        super().__init__(0, TxType.Deploy, gas_price, gas_limit, payer)
        if isinstance(code, str):
            code = bytearray.fromhex(code)
        self.__code = code
        if not isinstance(vm_type, VmType):
            raise SDKException(ErrorCode.other_error('invalid vm type'))
        self.__vm_type = vm_type
        self.__name = name
        self.__code_version = version
        self.__author = author
        self.__email = email
        self.__description = description

    def serialize_exclusive_data(self, writer: BinaryWriter):
        writer.write_var_bytes(self.__code)
        writer.write_byte(self.__vm_type.value)
        writer.write_var_str(self.__name)
        writer.write_var_str(self.__code_version)
        writer.write_var_str(self.__author)
        writer.write_var_str(self.__email)
        writer.write_var_str(self.__description)
