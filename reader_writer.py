from actors import Reader, Writer
from shmlib import SharedMemory
from multiprocessing import Process, Lock


def read_process(name: str, shm: SharedMemory):
    reader = Reader(name, shm)
    reader.mainloop()


def write_process(name: str, shm: SharedMemory, write_lock):
    writer = Writer(name, shm, write_lock)
    writer.mainloop()


def main(num_reader: int, num_writer: int, write_lock):
    sh_memory = SharedMemory(65)
    for i in range(1, num_reader + 1):
        name = f"Reader {i}"
        rproc = Process(target=read_process, args=(name, sh_memory))
        rproc.start()
    write_processes: list[Process] = []
    for i in range(1, num_writer + 1):
        name = f"Writer {i}"
        wproc = Process(target=write_process, args=(name, sh_memory, write_lock))
        wproc.start()
        write_processes.append(wproc)
    for wproc in write_processes:
        wproc.join()
    sh_memory.remove()


if __name__ == "__main__":
    num_reader = int(input("Input for number of readers: "))
    num_writer = int(input("Input for number of writers: "))
    write_lock = Lock()
    main(num_reader, num_writer, write_lock)
