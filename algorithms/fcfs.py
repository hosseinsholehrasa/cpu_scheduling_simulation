from process import State


class FCFS(object):

    def __init__(self, processes: list):
        """
        :param processes: list of processes sort by arrival time
        """
        self.processes = processes
        self.processes.sort(key=lambda process: process.arrival_time)
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
        timeline = 0.0
        cpu_idle_time = 0.0
        for process in self.processes:

            # cpu waiting time
            if process.arrival_time > timeline:
                cpu_idle_time += process.arrival_time - timeline
                # update time
                timeline = process.arrival_time

            # Run the process
            process.start_time = timeline

            # waiting, turnaround, response time
            process.waiting_time = timeline - process.arrival_time
            process.response_time = timeline - process.arrival_time
            process.turnaround_time = process.response_time + process.burst_time

            timeline += process.burst_time
            process.remaining_time -= process.burst_time
            process.end_time = timeline

            process.state = State.EXECUTED
            print(process)

            self.executed_processes.append(process)

        return {
            "executed_processes": self.executed_processes,
            "cpu_total_time": timeline,
            "cpu_idle_time": cpu_idle_time,
        }
