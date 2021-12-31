import random
import pandas as pd

from datetime import datetime
from process import Process
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

    @staticmethod
    def generate_processes_data(path: str, size: int = 1000, max_arrival_time: int = 1000) -> bool:
        """
        Generate process with random numbers for arrival and burst time and priority. then save it to a csv file
        :param max_arrival_time: maximum number for random number of arrival time
        :param path: path to save csv file
        :param size: number of processes
        :return: None
        """
        processes = []
        # save data as lists of lists then create dataframe. e.g [ [pid1, arrival1], [pid2, arrival2]]
        for i in range(size):
            processes.append([
                i,  # PID
                random.randint(0, max_arrival_time),  # arrival_time
                random.randint(0, 20),  # priority
                random.randint(0, 100),  # burst_time
            ])

        df = pd.DataFrame(processes, columns=['pid', 'arrival_time', 'priority', 'burst_time'])
        df.to_csv(path_or_buf=path, index=False)

        return True

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
