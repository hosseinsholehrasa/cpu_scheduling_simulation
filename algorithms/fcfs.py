from process import State


class FCFS(object):

    def __init__(self, processes: list):
        """
        :param processes: list of processes sort by arrival time
        """
        self.processes = processes
        self.processes.sort(key=lambda process: process.arrival_time)
        self.timeline = 0.0
        self.cpu_idle_time = 0.0
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

        for process in self.processes:

            # cpu waiting time
            if process.arrival_time > self.timeline:
                self.cpu_idle_time += process.arrival_time - self.timeline
                # update time
                timeline = process.arrival_time

            # Run the process
            process.start_time = self.timeline

            # waiting, turnaround, response time
            process.waiting_time = self.timeline - process.arrival_time
            process.response_time = self.timeline - process.arrival_time
            process.turnaround_time = process.response_time + process.burst_time

            self.timeline += process.burst_time
            process.remaining_time -= process.burst_time
            process.end_time = self.timeline

            process.state = State.EXECUTED
            print(process)

            self.executed_processes.append(process)

        return {
            "executed_processes": self.executed_processes,
            "cpu_total_time": self.timeline,
            "cpu_idle_time": self.cpu_idle_time,
        }
