#!/usr/bin/env python3


class Dictionary(dict):
    @classmethod
    def load(cls, f):
        import json
        if hasattr(f, 'read'):
            return json.load(f, object_hook=cls)
        else:
            with open(f, 'r') as fp:
                return json.load(fp, object_hook=cls)

    def where(self, expr):
        return Dictionary({k: v for k, v in self.items() if expr(k, v)})

    def select(self, expr):
        return List(expr(k, v) for k, v in self.items())

    def extend(self, **items):
        result = Dictionary(self) + Dictionary(items)
        return result

    def map_keys(self, expr):
        return Dictionary({expr(k): v for k, v in self.items()})

    def __dir__(self):
        return super().__dir__() + list(self.keys())

    def __getattr__(self, attr):
        x = self.get(attr)
        if type(x) is list:
            wrapped = List(x)
            self[attr] = wrapped
            return wrapped
        else:
            return x

    def __setattr__(self, attr, value):
        if type(value) is list:
            self[attr] = List(value)
        elif type(value) is dict:
            self[attr] = Dictionary(value)
        else:
            self[attr] = value

    def __add__(self, other):
        return merge_dicts(self, other)


class List(list):
    def where(self, expr):
        return List(x for x in self if expr(x))

    def select(self, expr=None):
        if callable(expr):
            return List(expr(x) for x in self)
        else:
            return List(x for x in self)

    def single(self):
        if len(self) != 1:
            raise ValueError('Length must be exactly 1')
        return self[0]

    def first(self):
        if len(self) < 1:
            raise IndexError('Length must be at least1')
        return self[0]

    def many(self, expr=None):
        result = []
        for x in self.select(expr):
            result.extend(x)
        return List(result)

    def join(self, others, expr, select=None):
        result = []
        select = select or merge_dicts
        for this in self:
            result.extend([select(this, other) for other in others if expr(this, other)])
        return List(result)


def merge_dicts(x, y):
    x_keys = set(x.keys())
    return Dictionary(**x, **{(k if k not in x_keys else k + '_'): v for k, v in y.items()})
