
import os
import json
import mmap
import numpy as np


class ip:

    def __init__(self, ipfile):

        euid = os.geteuid()
        if euid != 0:
            raise EnvironmentError('Root permissions required.')
        if not isinstance(ipfile, str):
            raise TypeError("IP file has to be a string.")
        if not os.path.isfile(ipfile):
            raise IOError("IP file {} dose not exist".format(ipfile))
        
        self._load_ipcfg(ipfile)
        self._mmapfile = os.open('/dev/mem', os.O_RDWR | os.O_SYNC)	
        self._virt_base = int(self._baseaddr, 16) & ~(mmap.PAGESIZE - 1)
        self._virt_offset = int(self._baseaddr, 16) - self._virt_base
        self._mem = mmap.mmap(self._mmapfile, int(self._length, 16) + self._virt_offset,
                             mmap.MAP_SHARED,
                             mmap.PROT_READ | mmap.PROT_WRITE,
                             offset=self._virt_base)
        self._load_regcfg(ipfile)


    def __del__(self):

        os.close(self._mmapfile)


    def _load_ipcfg(self, ipfile):

        with open(ipfile, 'r') as fp:
            data = json.load(fp)
            self._baseaddr = data['baseaddr']
            self._length = data['length']
       
 
    def _load_regcfg(self, ipfile):

       with open(ipfile, 'r') as fp:
            data = json.load(fp)
            for r in data['registars']:
                offset = int(r['offset'], 16) + self._virt_offset
                setattr(self, r['name'], self._reg(self._mem, offset, r['rwtype']))



    class _reg:
        
        def __init__(self, mem, offset, rwtype):

            self._rwtype = rwtype
            self._buf = np.frombuffer(mem, np.uint32, 1, offset)

        def __call__(self):

            if not 'R' in self._rwtype:
                raise TypeError('rwtype')
            return self._buf[0]

        def __call__(self, val):

            if not 'W' in self._rwtype:
                raise TypeError('rwtype')
            self._buf[0] = np.uint32(val)
            return self._buf[0]
            



