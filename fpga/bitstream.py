import os

BS_IS_PARTIAL = "/sys/devices/soc0/amba/f8007000.devcfg/is_partial_bitstream"
BS_XDEVCFG = "/dev/xdevcfg"


class bitstream(object):

    __instance = None


    def __new__(cls, *args, **kwargs):
        
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance


    def __init__(self, bitfile):

        if not isinstance(bitfile, str):
            raise TypeError("Bitstream file has to be a string.")

        if not os.path.isfile(bitfile):
            raise IOError("Bitstream file {} dose not exist".format(bitfile))
       
        self._bitfile = bitfile

    
    def download(self):
        
        with open(self._bitfile, 'rb') as f:
            buf = f.read()

        with open(BS_IS_PARTIAL, 'w') as fd:
            fd.write('0')

        with open(BS_XDEVCFG, 'wb') as f:
            f.write(buf)


