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

from typing import List, Union

from ontology.common.address import Address
from ontology.vm.build_params import BuildParams
from ontology.io.binary_reader import BinaryReader
from ontology.io.memory_stream import StreamManager
from ontology.exception.error_code import ErrorCode
from ontology.exception.exception import SDKException
from ontology.contract.neo.abi.struct_type import Struct
from ontology.contract.neo.params_builder import NeoParamsBuilder


class NeoData(object):
    @staticmethod
    def to_bool(hex_str) -> bool:
        if len(hex_str) != 2:
            raise SDKException(ErrorCode.other_error('invalid str'))
        return True if hex_str == '01' else False

    @staticmethod
    def get_map_bytes(param_dict: dict):
        builder = NeoParamsBuilder()
        builder.emit(BuildParams.Type.dict_type.value)
        builder.emit(NeoData.big_int_to_neo_bytearray(len(param_dict)))
        for key, value in param_dict.items():
            builder.emit(BuildParams.Type.bytearray_type.value)
            builder.push_bytearray(str(key).encode())
            if isinstance(value, bytearray) or isinstance(value, bytes):
                builder.emit(BuildParams.Type.bytearray_type.value)
                builder.push_bytearray(bytearray(value))
            elif isinstance(value, str):
                builder.emit(BuildParams.Type.bytearray_type.value)
                builder.push_bytearray(value.encode())
            elif isinstance(value, bool):
                builder.emit(BuildParams.Type.bool_type.value)
                builder.push_bool(value)
            elif isinstance(value, int):
                builder.emit(BuildParams.Type.int_type.value)
                builder.push_int(int(value))
            else:
                raise Exception("param error")
        return builder.to_bytes()

    @staticmethod
    def to_int(hex_str: str) -> int:
        if len(hex_str) == 0:
            return 0
        try:
            array = bytearray.fromhex(hex_str)
        except ValueError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        array.reverse()
        try:
            num = int(bytearray.hex(array), 16)
        except ValueError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        return num

    @staticmethod
    def op_code_to_int(op_code: str):
        if op_code.lower() == '4f':
            return -1
        elif op_code == '00':
            return 0
        elif 80 < int(op_code, base=16) < 103:
            return int(op_code, base=16) - 80
        else:
            op_code = bytearray.fromhex(op_code)
            stream = StreamManager.get_stream(op_code)
            reader = BinaryReader(stream)
            op_code = bytearray(reader.read_var_bytes())
            return NeoData.neo_bytearray_to_big_int(op_code)

    @staticmethod
    def to_int_list(hex_str_list: list) -> List[int]:
        for index, item in enumerate(hex_str_list):
            if isinstance(item, list):
                hex_str_list[index] = NeoData.to_int_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = NeoData.to_int(item)
            else:
                raise SDKException(ErrorCode.other_error('Invalid data.'))
        return hex_str_list

    @staticmethod
    def to_bytes(hex_str: str) -> bytes:
        try:
            bytes_str = bytes.fromhex(hex_str)
        except ValueError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        return bytes_str

    @staticmethod
    def to_bytes_list(hex_str_list: list) -> List[bytes]:
        for index, item in enumerate(hex_str_list):
            if isinstance(item, list):
                hex_str_list[index] = NeoData.to_bytes_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = NeoData.to_bytes(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_reserve_hex_str(hex_str: str) -> str:
        hex_str = ''.join(reversed([hex_str[i:i + 2] for i in range(0, len(hex_str), 2)]))
        return hex_str

    @staticmethod
    def to_utf8_str(ascii_str: str) -> str:
        try:
            utf8_str = bytes.fromhex(ascii_str)
            utf8_str = utf8_str.decode('utf-8')
        except ValueError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        return utf8_str

    @staticmethod
    def to_hex_str(ascii_str: str) -> str:
        hex_str = bytes.fromhex(ascii_str)
        return hex_str.decode('ascii')

    @staticmethod
    def to_utf8_str_list(hex_str_list: list) -> List[bytes]:
        for index, item in enumerate(hex_str_list):
            if isinstance(item, list):
                hex_str_list[index] = NeoData.to_utf8_str_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = NeoData.to_utf8_str(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_b58_address(hex_address: str) -> str:
        try:
            bytes_address = bytes.fromhex(hex_address)
        except ValueError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        address = Address(bytes_address)
        return address.b58encode()

    @staticmethod
    def to_b58_address_list(hex_str_list: list) -> List[bytes]:
        for index, item in enumerate(hex_str_list):
            if isinstance(item, list):
                hex_str_list[index] = NeoData.to_b58_address_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = NeoData.to_b58_address(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_bytes_address(hex_address: str) -> bytes:
        try:
            bytes_address = bytes.fromhex(hex_address)
        except ValueError as e:
            raise SDKException(ErrorCode.other_error(e.args[0]))
        address = Address(bytes_address)
        return address.to_bytes()

    @staticmethod
    def to_bytes_address_list(hex_str_list: list) -> List[bytes]:
        for index, item in enumerate(hex_str_list):
            if isinstance(item, list):
                hex_str_list[index] = NeoData.to_bytes_address_list(item)
            elif isinstance(item, str):
                hex_str_list[index] = NeoData.to_bytes_address(item)
            else:
                raise SDKException(ErrorCode.other_error('invalid data'))
        return hex_str_list

    @staticmethod
    def to_dict(item_serialize: str) -> dict:
        stream = StreamManager.get_stream(bytearray.fromhex(item_serialize))
        reader = BinaryReader(stream)
        return NeoData.__deserialize_stack_item(reader)

    @staticmethod
    def __deserialize_stack_item(reader: BinaryReader) -> dict or bytearray:
        param_type = reader.read_byte()
        if param_type == BuildParams.Type.bytearray_type.value:
            b = reader.read_var_bytes()
            return b
        elif param_type == BuildParams.Type.bool_type.value:
            return reader.read_bool()
        elif param_type == BuildParams.Type.int_type.value:
            b = reader.read_var_bytes()
            return NeoData.__big_int_from_bytes(bytearray(b))
        elif param_type == BuildParams.Type.struct_type.value or param_type == BuildParams.Type.array_type.value:
            count = reader.read_var_int()
            item_list = list()
            for _ in range(count):
                item = NeoData.__deserialize_stack_item(reader)
                item_list.append(item)
            if param_type == BuildParams.Type.struct_type.value:
                return Struct(item_list)
            return item_list
        elif param_type == BuildParams.Type.dict_type.value:
            count = reader.read_var_int()
            item_dict = dict()
            for _ in range(count):
                key = NeoData.__deserialize_stack_item(reader)
                value = NeoData.__deserialize_stack_item(reader)
                item_dict[key] = value
            return item_dict
        else:
            raise SDKException(ErrorCode.other_error('type error'))

    @staticmethod
    def __big_int_from_bytes(ba: bytearray):
        if len(ba) == 0:
            return 0
        ba_temp = ba[:]
        ba_temp.reverse()
        if ba_temp[0] >> 7 == 1:
            res = int.from_bytes(ba_temp, 'big', signed=True)
            return res
        return int.from_bytes(ba_temp, 'big', signed=True)

    @staticmethod
    def neo_bytearray_to_big_int(value: bytearray) -> int:
        if len(value) == 0:
            return 0
        ba_temp = value[:]
        ba_temp.reverse()
        if ba_temp[0] >> 7 == 1:
            res = int.from_bytes(ba_temp, 'big', signed=True)
            return res
        return int.from_bytes(ba_temp, 'big', signed=True)

    @staticmethod
    def big_int_to_neo_bytearray(data: int) -> bytearray:
        if data == 0:
            return bytearray()
        data_bytes = NeoData.int_to_bytearray(data)
        if len(data_bytes) == 0:
            return bytearray()
        if data < 0:
            data_bytes2 = NeoData.int_to_bytearray(-data)
            b = data_bytes2[0]
            data_bytes.reverse()
            if b >> 7 == 1:
                res = data_bytes[:] + bytearray([255])
                return res
            return data_bytes
        else:
            b = data_bytes[0]
            data_bytes.reverse()
            if b >> 7 == 1:
                res = data_bytes[:] + bytearray([0])
                return res
            return data_bytes

    @staticmethod
    def int_to_bytearray(data: int):
        bit_length = data.bit_length() // 8
        t = data.bit_length() / 8
        if bit_length <= t:
            bit_length += 1
        return bytearray(data.to_bytes(bit_length, "big", signed=True))

    @staticmethod
    def parse_addr_addr_int_notify(notify: dict):
        notify['States'][0] = NeoData.to_utf8_str(notify['States'][0])
        notify['States'][1] = NeoData.to_b58_address(notify['States'][1])
        notify['States'][2] = NeoData.to_b58_address(notify['States'][2])
        notify['States'][3] = NeoData.to_int(notify['States'][3])
        return notify
