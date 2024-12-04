from actors import Reader, Writer
from shmlib import SharedMemory
from multiprocessing import Process


def read_process(name: str, shm: SharedMemory):
    reader = Reader(name, shm)
    reader.mainloop()


def write_process(name: str, shm: SharedMemory):
    writer = Writer(name, shm)
    writer.mainloop()


def main():
    sh_memory = SharedMemory(65)
    NUM_READER = 1
    NUM_WRITER = 1
    for i in range(1, NUM_READER + 1):
        name = f"Reader {i}"
        rproc = Process(target=read_process, args=(name, sh_memory))
        rproc.start()
    write_processes: list[Process] = []
    for i in range(1, NUM_WRITER + 1):
        name = f"Writer {i}"
        wproc = Process(target=write_process, args=(name, sh_memory))
        wproc.start()
        write_processes.append(wproc)
    for wproc in write_processes:
        wproc.join()
    sh_memory.remove()


if __name__ == "__main__":
    main()
