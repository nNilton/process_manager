from enum import Enum


class ProcessStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'
    FAILED = 'FAILED'
    STOPPED = 'STOPPED'