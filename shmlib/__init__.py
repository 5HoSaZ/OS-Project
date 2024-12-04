import ctypes as C
from ctypes import CDLL

# Import C-defined functions in shmlib shared object
shmlib = CDLL("./shmlib/shmlib.so")

# Redefines function in Python
shmgen = shmlib.shmgen
shmgen.argtypes = [C.c_int]
shmgen.restype = C.c_int

shmwrite = shmlib.shmwrite
shmwrite.argtypes = [C.c_int, C.c_char_p]

shmread = shmlib.shmread
shmread.argtypes = [C.c_int]
shmread.restype = C.c_char_p

shmremove = shmlib.shmremove
shmremove.argtypes = [C.c_int]
shmremove.restype = C.c_int


# Shared memory class
class SharedMemory:
    """Shared memory class built from ctypes."""

    def __init__(self, id: int):
        self.__shmid = shmgen(id)

    def read(self) -> str:
        """Read text from shared memory."""
        btext: bytes = shmread(self.__shmid)
        return btext.decode()

    def write(self, text: str):
        """Write text to shared memory."""
        btext = text.encode()
        shmwrite(self.__shmid, btext)

    def remove(self) -> int:
        """Destroy the shared memory."""
        return shmremove(self.__shmid)
