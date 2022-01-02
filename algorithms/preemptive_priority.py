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

            arrived_processes = []
            # processes that their arrival time are equal to this timeline goes to ready queue
            for process in self.processes:
                if process.arrival_time == self.timeline:
                    arrived_processes.append(process)
                # for finishing sooner
                elif process.arrival_time > self.timeline:
                    break

            # for deleting new arrived processes from self.processes list
            for process in arrived_processes:
                if process in self.processes:
                    self.processes.remove(process)

            arrived_processes.sort(key=lambda p: p.priority)
            if arrived_processes:
                if self.running_process is None:
                    self.running_process = arrived_processes.pop(0)
                    self.running_process.start_time = self.timeline

                # new arrived processes have higher priority
                elif self.running_process.priority > arrived_processes[0].priority:
                    self.ready_queue.append(self.running_process)
                    self.running_process = arrived_processes.pop(0)
                    self.running_process.start_time = self.timeline

                # add arrived processes to ready queue
                self.ready_queue += arrived_processes

                # free this variable memory
                arrived_processes.clear()

                # sort ready queue when we have new processes that aren't in the list. otherwise, we have an sorted list
                self.ready_queue.sort(key=lambda p: p.priority)

            # If no process is running, then pick the process from ready queue, maybe a process has ran before
            if self.running_process is None and self.ready_queue:
                # we have an sorted ready queue
                self.running_process = self.ready_queue.pop(0)
                if self.running_process.start_time is None:
                    self.running_process.start_time = self.timeline
                else:
                    self.running_process.start_time = self.running_process.start_time

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

    def get_next_important_time(self):
        """
        Find next important things which happen in the timeline
        :return: Int
        """
        # we have deleted process from list when we decided about it to be an ready queue or running process
        future_processes = self.processes
        # we have an sorted ready queue

        if future_processes:
            # we have some conditions here. we have to compare ready queue and next process with their arrival time and
            # priority so just update time with 1
            if not self.running_process:
                return self.timeline + 1
            # if we have running process when we have future processes,
            # the important time is next arrival time or finishing the process
            return min(self.running_process.remaining_time + self.timeline, future_processes[0].arrival_time)
        else:
            if not self.running_process:
                return self.timeline + 1
            # we don't have new process and so we should wait until process finish it's work
            return self.running_process.remaining_time + self.timeline
