# !usr/bin/env python
# _*_ coding: utf-8 _*_
"""
    foo module for test
"""


class Foo:
    def __init__(self):
        return

    def bar(self, x):
        return x + 1

    def test(self):
        return 'test the python lib'


if __name__ == '__main__':
    foo = Foo()
    print(foo.bar(1))