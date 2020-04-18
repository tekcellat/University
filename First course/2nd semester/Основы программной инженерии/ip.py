def raise_f(arg):
    raise arg

class DefaultDict(dict):
    def __init__(self, default_factory=lambda key: raise_f(KeyError(key))):
        self.default_factory = default_factory
    def __missing__(self, key):
        value = self.default_factory(key)
        self[key] = value
        return value

@DefaultDict
def uint(length_in_bits):
    max_value = (1<<length_in_bits) - 1
    _type = type(
        'uint[{}]'.format(length_in_bits),
        (int,),
        dict(
            __slots__ = (),
            __repr__ = lambda self: "{}('{}')".format(type(self).__name__, self),
            __invert__ = lambda self: type(self)(self ^ max_value),
            # __lshift__ = lambda self, other: uint[length_in_bits](super(uint[length_in_bits], self).__lshift__(other) & max_value),
        )
    )
    def __new__(cls, arg=_type(0)):
        if isinstance(arg, cls):
            return arg
        else:
            _int = super(_type, cls).__new__(cls, arg)
            if 0 <= _int <= max_value:
                return _int
            else:
                raise ValueError('{} cannot be represented using only {} bits'.format(arg, length_in_bits))
    _type.__new__ = __new__
    return _type

from functools import reduce

class IPAddress(uint[32]):
    __slots__ = ()
    def _bytes(self):
        for i in range(24, -1, -8):
            yield (self>>i) & 0xFF
    def __str__(self):
        return '.'.join(map(str, self._bytes()))

    __IPAddress__ = lambda self: self

    __add__ = lambda self, other: super(IPAddress, type(self)).__new__(IPAddress, super(IPAddress, self).__add__(other))
    __sub__ = lambda self, other: super(IPAddress, type(self)).__new__(IPAddress, super(IPAddress, self).__sub__(other))
    __xor__ = lambda self, other: super(IPAddress, type(self)).__new__(IPAddress, super(IPAddress, self).__xor__(other))
    __or__  = lambda self, other: super(IPAddress, type(self)).__new__(IPAddress, super(IPAddress, self).__or__(other))
    __and__ = lambda self, other: super(IPAddress, type(self)).__new__(IPAddress, super(IPAddress, self).__and__(other))


    __mul__ = __truediv__ = __floordiv__ = __mod__ = __divmod__ = __pow__ = __abs__ = __pos__ = __neg__ = __complex__ = __float__ = __round__ = __floor__ = lambda *_, **__: raise_f(TypeError('Using this method on object of type IPAddress is not allowed.'))

# ip_address_dct = {name: lambda *_, **__: raise_f(TypeError) for name in ('__mul__', '__truediv__', '__floordiv__', '__mod__', '__divmod__', '__pow__', '__abs__', '__pos__', '__neg__', '__complex__', '__float__', '__round__', '__floor__')} # forbidden methods
# ip_address_dct.update(
#     {name: lambda self, other: super(IPAddress, type(self)).__new__(IPAddress, getattr(super(IPAddress, self), name)(other)) for name in ('__add__', '__sub__', '__xor__', '__or__', '__and__')},
#     _bytes  = lambda self: ((self>>i) & 0xFF for i in range(24, -1, -8)),
#     __str__ = lambda self: '.'.join(map(str, self._bytes())),
# )

# IPAddress = type(
#     'IPAddress',
#     (uint[32],),
#     ip_address_dct
# )


def ip_address__new__(cls, arg=IPAddress(0)):
    try:
        result = arg.__IPAddress__()
        if isinstance(result, cls):
            return result
        else:
            raise TypeError('{!r}.__IPAddress__() returned {!r}, when caller expected instance of {}.'.format(arg, result, cls))
    except AttributeError:
        pass
    _list = arg.split('.', 3)
    if len(_list) != 4:
        raise ValueError(repr(arg) + " does not represent four 8-bit integers separeted by dots.")
    return super(IPAddress, cls).__new__(cls, reduce(lambda x, y: (x<<8) | y, map(uint[8], _list)))
    

IPAddress.__new__ = ip_address__new__

class Mask(uint[5]):
    __slots__ = ()
    def _neg_bin(self):
        return uint[32].__new__(IPAddress, 0xFFFFFFFF >> self)
    def bin(self):
        return ~self._neg_bin()



class IPAddressWithMask(tuple):
    __slots__ = ()
    @property
    def ip_address(self):
        return self[0]
    @property
    def mask(self):
        return self[1]

    def __new__(cls, ip_address, mask=None):
        if mask is None:
            try:
                ip_address, mask = ip_address.split('/')
            except ValueError as e:
                raise ValueError(repr(ip_address) + ' does not represent valid IP address with mask.') from e
        return super(IPAddressWithMask, cls).__new__(cls, (IPAddress(ip_address), Mask(mask)))

    def network(self):
        return self.ip_address & self.mask.bin()
    def broadcast(self):
        return self.ip_address | self.mask._neg_bin()

    def __str__(self):
        return '{}/{}'.format(self.ip_address, self.mask)
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self)



if __name__ == '__main__':
    while True:
        try:
            line = input()
        except EOFError:
            break
        try:
            print('  input():', repr(line))
            ip_with_mask = IPAddressWithMask(line)
            print('   Parsed:', ip_with_mask)
            print('  Network:', ip_with_mask.network())
            print('Broadcast:', ip_with_mask.broadcast())
            print()
        except Exception as e:
            print('{}: {}\n'.format(type(e).__name__, e))
