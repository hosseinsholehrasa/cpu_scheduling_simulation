from process import State


class PreemptiveSFJ(object):
    """
    an algorithm which sort processes by the lowest burst time to the highest. It's a preemptive algorithm
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
