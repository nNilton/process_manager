import os
from tinydb import TinyDB, Query
from os import path, kill
from prettytable import PrettyTable
from subprocess import Popen, DEVNULL
from exceptions.ExecutionException import ExecutionException

class ProcessManager:

    def __init__(self) -> None:
        self.max_threads = os.cpu_count()
        self.threads_running = 0
        self.db = TinyDB("process_db.json")
        self.rp_table = self.db.table("running_processes")


    def process_monitor(self):
        pass

    def start_process(self, args):
        try:
            # File info vars
            procPath = path.abspath(args[0])
            procArgs = " ".join(args[1:])
            filename = path.basename(procPath)
            pass
        except Exception as ex:
            raise ExecutionException(f'Failed on starting process\n {str(ex)}')


    def stop_process(self):
        pass

    def kill_process(self):
        pass

    def list_processes(self):
        
        out_table = PrettyTable()
        out_table.hrules = True
        out_table.field_names = ["PID", "PName", "Args", "Status", "Path"]

        print("Process List\n")
        for proc in self.rp_table.all():
            out_table.add_row([proc["PID"], proc["PName"], proc["args"], proc['running'], proc["path"]])
        
        print(out_table)



    def remove_from_process_list(self):
        pass