from process import State


class NonPreemptivePriority(object):
    """
    an algorithm which sort processes by the highest priority to the lowest. It's a non-preemptive algorithm
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
                self.running_process.waiting_time = self.running_process.start_time - self.running_process.arrival_time
                self.running_process.response_time = self.running_process.start_time - self.running_process.arrival_time
                self.running_process.state = State.EXECUTED
                self.executed_processes.append(self.running_process)
                self.running_process = None

                # All processes have done
                if not (self.running_process or self.processes or self.ready_queue):
                    break

            new_arrived = []
            # processes that their arrival time are equal to this timeline goes to ready queue
            for process in self.processes:
                if process.arrival_time == self.timeline:
                    self.ready_queue.append(process)
                    new_arrived.append(process)
                # for finishing sooner
                elif process.arrival_time > self.timeline:
                    break
            # for deleting new arrived processes from self.processes list
            if new_arrived:
                self.remove_processes(new_arrived)

            self.ready_queue.sort(key=lambda p: p.priority)

            if self.running_process is None:
                # after sorting ready_queue by burst time, get first index and start to run that process
                self.running_process = self.ready_queue.pop(0)
                self.running_process.start_time = self.timeline
                self.running_process.state = State.RUNNING

            # run process until some important things happen
            next_important_time = self.get_next_important_time()
            if self.running_process:
                self.running_process.remaining_time -= (next_important_time - self.timeline)
            else:
                self.cpu_idle_time += (next_important_time - self.timeline)
            self.timeline = next_important_time

        return {
            "executed_processes": self.executed_processes,
            "cpu_total_time": self.timeline,
            "cpu_idle_time": self.cpu_idle_time,
        }

    def remove_processes(self, processes: list) -> bool:
        """
        Remove processes from self.processes list
        :param processes: list of processes
        :return: boolean
        """
        for process in processes:
            if process in self.processes:
                self.processes.remove(process)
        return True

    def get_next_important_time(self):
        """
        Find next important things which happen in the timeline
        :return: Int
        """
        # we have deleted process from list when we decided about it to be an ready queue or running process
        future_processes = self.processes

        # ready queue and future processes are sorted by arrival time
        if future_processes:
            # next process arrival time or next ready queue arrival time
            if not self.running_process:
                return min(future_processes[0].arrival_time, self.ready_queue[0].arrival_time)
            # if we have running_process so next process arrival time or remaining time to execute process
            else:
                return min(self.running_process.remaining_time + self.timeline, future_processes[0].arrival_time)
        # our processes have ended
        return self.running_process.remaining_time + self.timeline
