#!/user/env python3
# -*- coding: utf-8 -*-

import os

class Point:
    def __str__(self):
        return "<Point (x={}, y={})>".format(self.x, self.y)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __mul__(self, other):
        # 行列 ｘ Int
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def __matmul__(self, other):
        # 行列 ｘ 行列
        x = self.x * other.x
        y = self.y * other.y
        return Point(x, y)

    def serialize(self):
        return hex(self.x)[2:] + hex(self.y)[2:]


class LatticeEncrypt:
    def __init__(self, bit=16):
        self.bit = bit
        half = bit // 2
        self.sk = Point(self.random(bit), self.random(bit))  # bit bytes
        self.pk0 = Point(self.sk.x * self.random(half), self.sk.y * self.random(half))  # 1.5bit bytes
        self.pk1 = Point(self.sk.x * self.random(half), self.sk.y * self.random(half))  # 1.5bit bytes

    def encrypt(self, raw):
        bit = self.bit
        half = bit // 2
        assert isinstance(raw, bytes), 'raw is bytes'
        assert len(raw) == bit, 'raw is %d bytes' % bit
        m0, m1 = int.from_bytes(raw[:half], 'big'), int.from_bytes(raw[half:], 'big')  # 0.5bit bytes
        # print("m", m0, m1)
        p = Point(self.pk0.x * m0 + self.pk1.x * m1, self.pk0.y * m0 + self.pk1.y * m1)  # 2bit bytes
        # print("p", p)
        half = bit // 2
        r = Point(self.random(half), self.random(half))
        # print("r", r)
        c = p + r
        return c

    def decrypt(self, enc):
        bit = self.bit
        half = bit // 2
        m = Point(enc.x // self.sk.x, enc.y // self.sk.y)
        p = self.sk @ m
        # print("p", p)
        # p.x = pk0.x * m0 + pk1.x * m1
        # p.y = pk0.y * m0 + pk1.y * m1
        # 書き換えると
        # a = b * m0 + c * m1
        # d = e * m0 + f * m1
        #
        ae_bf = p.y * self.pk1.x - p.x * self.pk1.y
        cd_af = p.x * self.pk0.y - p.y * self.pk0.x
        ec_bf = self.pk0.y * self.pk1.x - self.pk0.x * self.pk1.y
        if ae_bf % ec_bf != 0 or cd_af % ec_bf != 0:
            raise ValueError('decrypt failed.')
        m0 = ae_bf // ec_bf
        m1 = cd_af // ec_bf
        # print("m", m0, m1)
        return m0.to_bytes(half, 'big') + m1.to_bytes(half, 'big')

    @staticmethod
    def random(bit):
        return int.from_bytes(os.urandom(bit), 'big')


def test():
    le = LatticeEncrypt()
    print("sk", le.sk.serialize())
    print("pk0", le.pk0.serialize())
    print("pk1", le.pk1.serialize())
    raw = os.urandom(16)
    enc = le.encrypt(raw)
    print("enc", enc)
    dec = le.decrypt(enc)
    print("result", dec == raw)

if __name__ == '__main__':
    test()
