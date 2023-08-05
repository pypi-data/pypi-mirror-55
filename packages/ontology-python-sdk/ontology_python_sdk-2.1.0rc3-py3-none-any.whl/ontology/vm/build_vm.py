"""
Copyright (C) 2018-2019 The ontology Authors
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

from ontology.vm.op_code import *
from ontology.common.address import Address
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.contract.neo.params_builder import NeoParamsBuilder


def build_native_invoke_code(contract_address: bytes, version: bytes, method: str, params):
    builder = NeoParamsBuilder()
    build_neo_vm_param(builder, params)
    builder.push_bytearray(method.encode())
    builder.push_bytearray(contract_address)
    builder.push_int(int.from_bytes(version, 'little'))
    builder.emit(SYSCALL)
    builder.push_bytearray(b'Ontology.Native.Invoke')
    return builder.to_bytes()


def build_neo_vm_param(builder, params):
    if isinstance(params, dict):
        builder.push_int(0)
        builder.emit(NEWSTRUCT)
        builder.emit(TOALTSTACK)
        for i in params.values():
            build_neo_vm_param(builder, i)
            builder.emit(DUPFROMALTSTACK)
            builder.emit(SWAP)
            builder.emit(APPEND)
        builder.emit(FROMALTSTACK)
    elif isinstance(params, str):
        builder.push_bytearray(params.encode('utf-8'))
    elif isinstance(params, bytes):
        builder.push_bytearray(params)
    elif isinstance(params, bytearray):
        builder.push_bytearray(params)
    elif isinstance(params, int):
        builder.push_int(params)
    elif isinstance(params, Address):
        builder.push_bytearray(params.to_bytes())
    elif isinstance(params, list):
        for p in params:
            build_neo_vm_param(builder, p)
        builder.push_int(len(params))
        builder.emit(PACK)
    else:
        raise SDKException(ErrorCode.param_error)
