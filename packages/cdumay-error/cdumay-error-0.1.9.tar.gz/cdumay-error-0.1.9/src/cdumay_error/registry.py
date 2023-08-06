#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@corp.ovh.com>


"""
from collections import OrderedDict


class Registry(object):
    ERRORS = list()

    @classmethod
    def register(cls, clazz):
        if clazz not in cls.ERRORS:
            cls.ERRORS.append(clazz)
        return clazz

    @classmethod
    def filter_by_status(cls, code):
        return [x for x in cls.ERRORS if x.CODE == code]

    @staticmethod
    def error_to_dict(clazz):
        return dict(
            code=clazz.CODE, description=clazz.__doc__, msgid=clazz.MSGID,
            name=clazz.__name__
        )

    @classmethod
    def to_list(cls):
        return [cls.error_to_dict(x) for x in cls.ERRORS]

    @classmethod
    def to_dict(cls):
        return OrderedDict([
            (x.MSGID, cls.error_to_dict(x))
            for x in sorted(cls.ERRORS, key=lambda x: x.MSGID)
        ])
