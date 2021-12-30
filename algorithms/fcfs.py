from process import State


class FCFS(object):

    def __init__(self, processes: list):
        """
        :param processes: list of processes sort by arrival time
        """
        self.processes = list(processes).sort(key=lambda process: process.arrival_time)
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
        total_time = 0.0
        cpu_idle_time = 0.0
        while self.processes:
            process = self.processes.pop(0)

            # cpu waiting time
            if process.arrival_time > total_time:
                cpu_idle_time += process.arrival_time - total_time
                # update time
                total_time = process.arrival_time

            # waiting time
            process.waiting_time = total_time - process.arrival_time
            # turnaround time
            process.turnaround_time = process.response_time + process.burst_time
            # response time
            process.response_time = total_time - process.arrival_time

            # Run the process
            process.start_time = total_time
            total_time += process.burst_time
            process.remaining_time -= process.burst_time
            process.end_time = total_time

            # be sure that process finished
            if process.remaining_time == 0:
                process.state = State.EXECUTED
                self.executed_processes.append(process)

        self.suspended_processes = self.processes

        return {
            "executed_processes": self.executed_processes,
            "total_time": total_time,
            "cpu_idle_time": cpu_idle_time,
        }
