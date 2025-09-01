# This file is part of 'NTLM Authorization Proxy Server'
# Copyright 2001 Dmitry A. Rozmanov <dima@xenon.spb.ru>
#
# NTLM APS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# NTLM APS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the sofware; see the file COPYING. If not, write to the
# Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#

hd = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',]

#--------------------------------------------------------------------------------------------
def str2hex_num(s):
    res = 0
    for i in s:
        res = res << 8
        # Handle both bytes (int) and string (char) in Python 3
        if isinstance(i, int):
            res = res + int(i)
        else:
            res = res + int(ord(i))
    return hex(res)

#--------------------------------------------------------------------------------------------
def str2hex(s, delimiter=''):
    res = ''
    for i in s:
        # Handle both bytes (int) and string (char) in Python 3
        if isinstance(i, int):
            o = i
        else:
            o = ord(i)
        res = res + hd[o // 16]
        res = res + hd[o % 16]
        res = res + delimiter
    return res

#--------------------------------------------------------------------------------------------
def str2dec(s, delimiter=''):
    res = ''
    for i in s:
        # Handle both bytes (int) and string (char) in Python 3
        if isinstance(i, int):
            res = res + '%3d' % i
        else:
            res = res + '%3d' % ord(i)
        res = res + delimiter
    return res


#--------------------------------------------------------------------------------------------
def hex2str(hex_str):
    res = ''
    for i in range(0, len(hex_str), 2):
        res = res + chr(hd.index(hex_str[i]) * 16 + hd.index(hex_str[i+1]))
    return res

#--------------------------------------------------------------------------------------------
def str2prn_str(bin_str, delimiter=''):
    res = ''
    for i in bin_str:
        # Handle both bytes (int) and string (char) in Python 3
        if isinstance(i, int):
            if i > 31: res = res + chr(i)
            else: res = res + '.'
        else:
            if ord(i) > 31: res = res + i
            else: res = res + '.'
        res = res + delimiter
    return res

#--------------------------------------------------------------------------------------------
def byte2bin_str(char):
    res = ''
    # Handle both characters and integers
    if isinstance(char, int):
        t = char
    else:
        t = ord(char)
    while t > 0:
        t1 = t // 2
        if t != 2 * t1: res = '1' + res
        else: res = '0' + res
        t = t1
    if len(res) < 8: res = '0' * (8 - len(res)) + res
    return res

#--------------------------------------------------------------------------------------------
def str2lst(s):
    res = []
    for i in s:
        # Handle both bytes (int) and string (char) in Python 3
        if isinstance(i, int):
            res.append(i)
        else:
            res.append(ord(i))
    return res

#--------------------------------------------------------------------------------------------
def lst2str(lst):
    res = ''
    for i in lst:
        res = res + chr(i & 0xFF)
    return res

#--------------------------------------------------------------------------------------------
def int2chrs(number_int):
    return chr(number_int & 0xFF) + chr((number_int >> 8) & 0xFF)

#--------------------------------------------------------------------------------------------
def bytes2int(b):
    # Handle both bytes (int) and string (char) in Python 3
    if isinstance(b[0], int):
        return b[1] * 256 + b[0]
    else:
        return ord(b[1]) * 256 + ord(b[0])

#--------------------------------------------------------------------------------------------
def int2hex_str(number_int16):
    res = '0x'
    ph = int(number_int16) // 256
    res = res + hd[ph // 16]
    res = res + hd[ph % 16]

    pl = int(number_int16) - (ph * 256)
    res = res + hd[pl // 16]
    res = res + hd[pl % 16]

    return res

#--------------------------------------------------------------------------------------------
def str2unicode(string):
    # In Python 3, all strings are unicode, but for NTLM, we may need UTF-16LE encoding
    if isinstance(string, str):
        return string.encode('utf-16le')
    return string

