from multiprocessing import Process, Lock, Value, Event
from shmlib import SharedMemory
from actors import User


class Monitor:
    def __init__(self, user_count: int, read_events: list):
        # User counter
        self.num_users = Value("i", user_count)
        # Read counter
        self.counter = Value("i", 0)
        # Write mutex
        self.write_lock = Lock()
        # All read events
        self.read_events = read_events
        # Shared memory
        self.shm = SharedMemory(67)

    def signal_new_msg(self):
        with self.counter.get_lock():
            # Reset the counter
            self.counter.value = int(self.num_users.value)
            # Set all processes to read
            for event in self.read_events:
                event.set()

    def user_exit(self, exit_text: str):
        # Exit only when write lock is on
        self.write_lock.acquire()
        with self.num_users.get_lock():
            self.num_users.value -= 1
        self.write_lock.release()
        self.shm_write(exit_text)

    def shm_read(self) -> str:
        with self.counter.get_lock():
            # Read once
            self.counter.value -= 1
            # Get new message
            msg = self.shm.read()
            # Release the write lock when all processes have read the new message
            if self.counter.value == 0:
                self.write_lock.release()
        return msg

    def shm_write(self, msg: str):
        # Acquire write lock
        self.write_lock.acquire()
        # Write to shared memory
        self.shm.write(msg)
        # Signal new message sent
        self.signal_new_msg()

    def close(self):
        self.shm.remove()


def user_process(name: str, monitor: Monitor, event):
    User(name, monitor, event).mainloop()


if __name__ == "__main__":
    user_count = int(input("Number of users: "))

    events = [Event() for _ in range(user_count)]
    monitor = Monitor(user_count, events)

    user_processes = [
        Process(
            target=user_process,
            args=(
                f"User {i + 1}",
                monitor,
                events[i],
            ),
        )
        for i in range(user_count)
    ]
    for process in user_processes:
        process.start()
    for process in user_processes:
        process.join()
    monitor.close()
