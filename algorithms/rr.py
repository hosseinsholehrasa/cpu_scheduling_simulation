from process import State


class RR(object):
    """
    an algorithm which each process have a quantum time to run after that is preempted and added to end of ready queue.
    It's a preemptive algorithm
    """

    def __init__(self, processes: list, quantum_number: int = 4):
        """
        :param processes: list of processes sort by arrival time
        :param quantum_number: limitation number for execution time of each process
        """
        self.quantum_number = quantum_number
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

            # a running process have done its work
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

            # update ready queue with new arrival time processes in this timeline
            self.update_ready_queue(self.timeline)

            if self.running_process is None and self.ready_queue:
                self.running_process = self.ready_queue.pop(0)
                if self.running_process.start_time is None:
                    self.running_process.start_time = self.timeline
                else:
                    self.running_process.start_time = self.running_process.start_time
                self.running_process.state = State.RUNNING

            if self.running_process:
                # after finishing this part, in next loop, the process waiting_time and other attr is calculated.
                # then next process in ready queue will replace running_process
                if self.running_process.remaining_time <= self.quantum_number:
                    added_time = self.running_process.remaining_time
                    self.running_process.remaining_time -= added_time
                    # update ready queue with new processes before this process be end
                    for future_time in range(1, added_time + 1):
                        timeline = self.timeline + future_time
                        self.update_ready_queue(timeline)
                else:
                    added_time = self.quantum_number
                    self.running_process.remaining_time -= added_time

                    # update ready queue before add this process to end of ready queue
                    for future_time in range(1, added_time + 1):
                        timeline = self.timeline + future_time
                        self.update_ready_queue(timeline)

                    self.ready_queue.append(self.running_process)
                    self.running_process = None

            else:
                added_time = 1
                self.cpu_idle_time += added_time
            self.timeline += added_time

        return {
            "executed_processes": self.executed_processes,
            "cpu_total_time": self.timeline,
            "cpu_idle_time": self.cpu_idle_time,
        }

    def update_ready_queue(self, timeline):
        """
        update ready queue with self.processes which are in this timeline
        :param timeline: timeline that we want to compare with new processes arrival time
        :return:
        """
        arrived_processes = []
        # processes that their arrival time are equal to this timeline goes to ready queue
        for process in self.processes:
            if process.arrival_time == timeline:
                self.ready_queue.append(process)
                arrived_processes.append(process)
            # for finishing sooner
            elif process.arrival_time > self.timeline:
                break

        # for deleting new arrived processes from self.processes list
        for process in arrived_processes:
            if process in self.processes:
                self.processes.remove(process)
        arrived_processes.clear()
