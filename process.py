class State:
    """ Process states enum """
    WAITING = 0
    READY = 1
    RUNNING = 2
    TERMINATED = 3
    SUSPENDED = 4
    EXECUTED = 5
    NEW = 6

    def __init__(self):
        self.state = self.NEW

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def __str__(self):
        translated_enums = {
            0: 'waiting', 1: 'ready', 2: 'running', 3: 'terminated',
            4: 'suspended', 5: 'executed', 6: 'new'
        }
        return translated_enums[self.state]


class Process:
    def __init__(self, pid, arrival_time, priority, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.priority = priority
        self.burst_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

    def __str__(self):
        return f"pid: {self.pid} | arrival_time: {self.arrival_time} | priority: {self.priority}"

