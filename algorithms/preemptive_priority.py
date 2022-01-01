from process import State


class PreemptivePriority(object):
    """
    an algorithm which sort processes by the highest priority to the lowest. It's a preemptive algorithm
    """

    def __init__(self, processes: list):
        """
        :param processes: list of processes sort by arrival time
        """
        self.processes = processes
        self.processes.sort(key=lambda process: process.arrival_time)
        self.timeline = 0.0
        self.cpu_idle_time = 0.0
        self.running_process = None
        self.ready_queue = []
        self.executed_processes = []
        self.suspended_processes = []

    def run(self) -> dict:
        """
        For running the algorithm
        :return {
            "executed_processes": list of executed processes,
            "total_time": total time of execution,
            "cpu_idle_time": time that cpu was idle,
        }
        """

        while self.processes or self.ready_queue or self.running_process:

            # a running process have done
            if self.running_process and self.running_process.remaining_time == 0:
                self.running_process.end_time = self.timeline
                # calculate turnaround and waiting and response time
                self.running_process.turnaround_time = self.running_process.end_time - self.running_process.arrival_time
                self.running_process.waiting_time = self.running_process.turnaround_time - self.running_process.burst_time
                self.running_process.response_time = self.running_process.start_time - self.running_process.arrival_time
                self.running_process.state = State.EXECUTED
                self.executed_processes.append(self.running_process)
                self.running_process = None

                # All processes have done
                if not (self.running_process or self.processes or self.ready_queue):
                    break
