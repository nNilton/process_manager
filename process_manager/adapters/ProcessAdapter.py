from enums.ProcessStatus import ProcessStatus

class ProcessAdapter():

    def __init__(self, pid, name, priority, create_time, memory_usage, n_threads, path) -> None:
        self.pid = pid
        self.name = name
        self.priority = priority
        self.create_time = create_time
        self.memory_usage = memory_usage
        self.n_threads = n_threads
        self.path = path
        self.__process_status = ProcessStatus.SCHEDULED

    def get_process_status(self):
        return self.__process_status