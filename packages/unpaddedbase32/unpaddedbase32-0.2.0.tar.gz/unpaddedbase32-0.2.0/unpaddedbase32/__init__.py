"""
    unpaddedbase32. Use base32 without padding in Python
    Copyright (C) 2019 Kevin Froman

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Union
import base64

def b32encode(data):
    """Simply base32 encodes data and removes the = padding"""
    data: bytes
    return base64.b32encode(data).replace(b"=", b"")

def b32decode(data):
    """Repad base32 bytes string, then decode it and return the result"""
    data: bytes
    data = repad(data)
    data = base64.b32decode(data)
    return data

def repad(data: Union[str, bytes])->Union[str, bytes]:
    """Repad a base32 string if necessary"""
    padding_char = "="
    if type(data) is bytes: 
        padding_char = b"="

    if not padding_char in data:
        padding = 8 - (len(data) % 8)
        data = data + (padding_char * padding)
    return data
