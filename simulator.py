import random
import pandas as pd
import algorithms
import time

from process import Process


def get_cpu_time_unit():
    """
    a unit of time independent on cpu run this code for simulating time
    """

    started_at = time.time()
    for i in range(1, 10000):
        if i % 2 == 0:
            temp = i / 2
        else:
            temp = 2 * i

    ended_at = time.time()
    return ended_at - started_at


class Simulator:

    def __init__(self, algorithm: str):
        self.algorithm = algorithm
        self.algorithm_class = self.get_algorithm_class()
        self.processes = []
        self.total_process = 0
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
        :return: bool
        """
        data = []
        # save data as lists of lists then create dataframe. e.g [ [pid1, arrival1], [pid2, arrival2]]
        for i in range(size):
            data.append([
                i + 1,  # PID
                random.randint(0, max_arrival_time),  # arrival_time
                random.randint(0, 20),  # priority
                random.randint(0, 100),  # burst_time
            ])

        df = pd.DataFrame(data, columns=['pid', 'arrival_time', 'priority', 'burst_time'])
        df.to_csv(path_or_buf=path, index=False)

        return True

    def read_processes_data(self, path=None, dataframe=None) -> bool:
        """
        read data from csv file or pandas dataframe
        one of path or dataframe parms needed
        :param path: string path of your csv file
        :param dataframe: you can pass dataframe object
        :return: a true boolean if everythings goes right
        """
        if isinstance(dataframe, pd.DataFrame):
            df = dataframe
        elif path and path.split('.')[-1] == 'csv':
            df = pd.read_csv(path)
        else:
            raise Exception("Your file should be a csv format or pass dataframe object to function")

        for i in range(0, df['pid'].count()):
            process = Process(
                pid=df['pid'][i],
                arrival_time=df['arrival_time'][i],
                priority=df['priority'][i],
                burst_time=df['burst_time'][i]
            )
            self.processes.append(process)

        return True

    def get_algorithm_class(self):
        """
        find algorithm class based on algorithm folder
        :return a class
        """
        try:
            return getattr(algorithms, self.algorithm)
        except Exception as e:
            print(e)
            raise Exception("try again! you have to enter a valid algorithm")

    def run(self):
        """
        Simulate algorithm and save the result of it
        """

        if len(self.processes) == 0:
            raise Exception("you have to load processes")

        # algorithm instance. need process list object
        algorithm = self.algorithm_class(self.processes)

        start_time = time.time()
        # run algorithm
        result = algorithm.run()
        end_time = time.time()
        self.run_time = end_time - start_time

        # set result of simulation
        # this processes referred to executed processes in output of algorithm run
        processes = result['executed_processes']
        total_process = len(processes)
        cpu_total_time = result['cpu_total_time']

        throughput = total_process / cpu_total_time
        cpu_utilization = (cpu_total_time - result['cpu_idle_time']) / cpu_total_time

        average_waiting_time = sum(process.waiting_time for process in processes) / total_process
        average_turnaround_time = sum(process.turnaround_time for process in processes) / total_process
        average_response_time = sum(process.response_time for process in processes) / total_process

        self.total_process = total_process
        self.cpu_total_time = cpu_total_time
        self.throughput = throughput
        self.cpu_utilization = cpu_utilization
        self.average_waiting_time = average_waiting_time
        self.average_turnaround_time = average_turnaround_time
        self.average_response_time = average_response_time

    def __str__(self):
        return {
            "total_process": self.total_process,
            "run_time": self.run_time,
            "cpu_total_time": self.cpu_total_time,
            "throughput": self.throughput,
            "cpu_utilization": self.cpu_utilization,
            "average_waiting_time": self.average_waiting_time,
            "average_turnaround_time": self.average_turnaround_time,
            "average_response_time": self.average_response_time
        }


if __name__ == '__main__':
    algorithm = input("algorithm name")
    simulate = Simulator(algorithm)
    simulate.read_processes_data("test.csv")
    simulate.run()
    print(simulate.__str__())
