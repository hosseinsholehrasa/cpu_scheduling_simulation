from process import State


class NonPreemptiveSFJ(object):
    """
    an algorithm which sort processes by the lowest burst time to the highest. It's a non-preemptive algorithm
    """

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
