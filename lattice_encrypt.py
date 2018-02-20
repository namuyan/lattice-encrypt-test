#!/user/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from binascii import hexlify, unhexlify
import math


class Serial:
    @staticmethod
    def serialize(key, byte=None):
        if byte:
            return hexlify(b''.join(int(n).to_bytes(byte, 'big') for n in key)).decode()
        else:
            byte = max(math.floor(math.log(n, 256)) for n in key) + 1
            return hexlify(byte.to_bytes(1, 'big') + b''.join(int(n).to_bytes(byte, 'big') for n in key)).decode()

    @staticmethod
    def deserialize(hex_str, byte=None):
        hex_bin = unhexlify(hex_str.encode())
        if byte is None:
            byte, hex_bin = hex_bin[0], hex_bin[1:]
        return np.array([int.from_bytes(hex_bin[byte * n:byte * (n + 1)], 'big')
                        for n in range(len(hex_bin) // byte)], dtype=np.uint64)


class LatticeEncrypt:
    def __init__(self, dim=2, byte=4):
        self.dim = dim
        self.byte = byte

    def create_key(self):
        byte = self.byte
        dim = self.dim
        sk = np.array([self.random(byte, min=255) for n in range(dim)], dtype=np.uint64)  # N行1列, 1n bytes
        pk = np.array([sk[n % dim] * self.random(byte) for n in range(dim**2)]
                      , dtype=np.uint64)  # .transpose()  # N行N列, 2n bytes
        return Serial.serialize(sk, byte), Serial.serialize(pk, byte*2)

    def encrypt(self, pk, raw):
        assert isinstance(raw, bytes), 'raw is bytes'
        assert len(raw) == self.dim * self.byte, 'need %d bytes' % self.dim * self.byte
        pk = Serial.deserialize(pk, self.byte*2)
        byte = self.byte
        dim = self.dim
        m = np.array([int.from_bytes(raw[byte * n: byte * (n + 1)], 'big') for n in range(self.dim)]
                     , dtype=np.uint64)
        # print("m", m)
        p = np.dot(m, pk.reshape((dim, dim)))  # N行1列
        # print("p", p)
        r = np.array([self.random(1) for n in range(dim)], dtype=np.uint64)
        # print("r", r)  # rはskより小さくなくてはならない
        enc = Serial.serialize(p + r)
        return enc

    def decrypt(self, sk, pk, enc):
        pk = Serial.deserialize(pk, self.byte * 2)
        sk = Serial.deserialize(sk, self.byte)
        enc = Serial.deserialize(enc)
        dim = self.dim
        s = np.array([enc[n] // sk[n] for n in range(dim)], dtype=np.uint64)
        # print('s', s)
        p = np.array([s[n] * sk[n] for n in range(self.dim)], dtype=np.uint64)
        # print('p', p)
        m = np.linalg.solve(pk.reshape((dim, dim)).transpose(), p)
        # print("m", m)
        raw = b''.join([int(round(m[n])).to_bytes(self.byte, 'big') for n in range(dim)])
        return raw

    @staticmethod
    def random(bit, min=None):
        while True:
            i = int.from_bytes(os.urandom(bit), 'big')
            if min is None or i > min:
                return i


def test():
    dim, byte = 600, 2
    le = LatticeEncrypt(dim, byte)
    sk, pk = le.create_key()
    print("sk", len(sk) // 2, 'bytes')
    print("pk", len(pk) // 2 / 1000, 'k bytes')

    raw = os.urandom(dim*byte)
    enc = le.encrypt(pk, raw)
    print("enc", len(enc), 'bytes')
    dec = le.decrypt(sk, pk, enc)
    print("result", dec == raw)

if __name__ == '__main__':
    test()
