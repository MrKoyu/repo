from Crypto.Cipher.blockcipher import *
from Crypto.Cipher.Rijndael import RijndaelCipher


def new(key, mode=MODE_ECB, IV=None, counter=None, segment_size=None):
    return AES(key, mode, IV, counter, segment_size)


class AES(BlockCipher):
    def __init__(self, key, mode, IV, counter, segment_size):
        self.blocksize = 16
        BlockCipher.__init__(self, key, mode, IV, counter, RijndaelCipher, segment_size)

    def keylen_valid(self, key):
        return len(key) in (16, 24, 32)

block_size = 16
