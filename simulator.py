from datetime import datetime
import algorithms


def get_cpu_time_unit():
    """
    a unit of time independent on cpu run this code for simulating time
    """

    started_at = datetime.now()
    for i in range(1, 10000):
        if i % 2 == 0:
            temp = i / 2
        else:
            temp = 2 * i

    ended_at = datetime.now()
    return ended_at - started_at


class Simulator:

    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.processes = []
        self.run_time = 0
        self.cpu_total_time = 0
        self.cpu_utilization = 0
        self.throughput = 0
        self.average_waiting_time = 0.0
        self.average_turnaround_time = 0.0
        self.average_response_time = 0.0

    def read_processes_data(self, data_dir: str, dataframe=None) -> list:
        """
        read data from csv file or pandas dataframe
        :return a list of process object:
        """
        pass

    def get_algorithm(self):
        """
        find algorithm class based on algorithm folder
        :return a class
        """
        try:
            return getattr(algorithms, self.algorithm)
        except Exception as e:
            print(e)
            print("try again!")
            exit()

