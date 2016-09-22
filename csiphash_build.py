import os

from cffi import FFI


siphash_source_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'siphash24.c')

ffibuilder = FFI()
ffibuilder.cdef('''int siphash(uint8_t *out, const uint8_t *in, uint64_t inlen, const uint8_t *k);''')

with open(siphash_source_file) as siphash_source:
    ffibuilder.set_source('csiphash._siphash', siphash_source.read())


if __name__ == '__main__':
    ffibuilder.compile(verbose=True)
