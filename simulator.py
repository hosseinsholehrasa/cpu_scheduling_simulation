import random
import time
import algorithms  # local module
import pandas as pd
from graphics import graphic as simulation_graphic

from process import Process
from pathlib import Path


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
        """
        run_time attr is for running algorithm in second
        cpu_total_time is total time of running processes for cpu. The number doesn't have any unit
        cpu_run_time attr total time of running processes for cpu. unit of time depend on get_cpu_time_unit function

        :param algorithm: algorithm name that valid in algorithm list
        """
        self.algorithm = algorithm
        self.algorithm_class = self.get_algorithm_class()
        self.algorithms_list = ["FCFS", "NonPreemptiveSFJ", "PreemptiveSFJ", "RR",
                                "NonPreemptivePriority", "PreemptivePriority"]
        self.processes = []
        self.total_process = 0
        self.run_time = 0
        self.cpu_run_time = 0
        self.cpu_total_time = 0
        self.cpu_utilization = 0
        self.throughput = 0
        self.average_waiting_time = 0.0
        self.average_turnaround_time = 0.0
        self.average_response_time = 0.0

    def _compress_df_rows(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        you can compress your dataframe based on your column name.
        for example you have 1000 rows that their priority column have value of 0
        so you average values of all other columns and compress 1000 rows to one
        :param df: dataframe which you want to compress same column values
        :param column: the column that you want to compress values
        :return: compressed dataframe
        """
        # raise error if column not in compress columns
        if column not in ('priority', 'burst_time', 'arrival_time'):
            raise KeyError("Your column not valid")

        df = df.sort_values(column, ignore_index=True)
        unique_columns = list(df[column].unique())

        data = []
        # compress column based on column name
        if column == "priority":
            # mean over each priority
            for c in unique_columns:
                result = df.where(df[column] == c).mean(numeric_only=True)
                data.append([
                    result['waiting_time'],
                    result['turnaround_time'],
                    result['response_time']
                ])
            # create dataframe
            compress_df = pd.DataFrame(
                data,
                columns=['waiting_time', 'turnaround_time', 'response_time'],
                index=unique_columns)

        elif column == "burst_time":

            # divide variety of the column to 20 part and create range of numbers instead of a number
            pieces = 20 if len(unique_columns) > 20 else 1
            batches = len(unique_columns) // pieces
            index_ranges = []

            for c in range(pieces + 1):
                low_range = batches * c
                high_range = batches * (c + 1)
                # mean over the ranges
                result = df.where((low_range <= df[column]) & (df[column] < high_range)).mean(numeric_only=True)
                data.append([
                    result['waiting_time'],
                    result['turnaround_time'],
                    result['response_time']
                ])

                # create index ranges for creating index of dataframe
                index_ranges.append(f"{low_range}-{high_range}")

            # create dataframe
            compress_df = pd.DataFrame(
                data,
                columns=['waiting_time', 'turnaround_time', 'response_time'],
                index=index_ranges)

        elif column == "arrival_time":
            # divide variety of the column to 20 part and create range of numbers instead of a number
            pieces = 20 if len(unique_columns) > 20 else 1
            batches = len(unique_columns) // pieces
            index_ranges = []

            for c in range(pieces + 1):
                low_range = batches * c
                high_range = batches * (c + 1)
                # mean over the ranges
                result = df.where((low_range <= df[column]) & (df[column] < high_range)).mean(numeric_only=True)
                data.append([
                    result['waiting_time'],
                    result['turnaround_time'],
                    result['response_time']
                ])

                # create index ranges for creating index of dataframe
                index_ranges.append(f"{low_range}-{high_range}")

            # create dataframe
            compress_df = pd.DataFrame(
                data,
                columns=['waiting_time', 'turnaround_time', 'response_time'],
                index=index_ranges)

        return compress_df

    def set_algorithm(self, algorithm: str) -> bool:
        """
        changing algorithm and validate algorithm
        :param algorithm: new algorithm name
        :return: True if has changed
        """
        self.algorithm = algorithm
        self.algorithm_class = self.get_algorithm_class()
        return True

    @staticmethod
    def generate_processes_data(path: str = 'data.csv', size: int = 1000, max_arrival_time: int = 1000) -> bool:
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

    def read_processes_data(self, path='data.csv', dataframe=None) -> bool:
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
        cpu_run_time = cpu_total_time * get_cpu_time_unit()
        throughput = total_process / cpu_total_time
        cpu_utilization = (cpu_total_time - result['cpu_idle_time']) / cpu_total_time

        average_waiting_time = sum(process.waiting_time for process in processes) / total_process
        average_turnaround_time = sum(process.turnaround_time for process in processes) / total_process
        average_response_time = sum(process.response_time for process in processes) / total_process

        self.total_process = total_process
        self.cpu_total_time = cpu_total_time
        self.cpu_run_time = cpu_run_time
        self.throughput = throughput
        self.cpu_utilization = cpu_utilization
        self.average_waiting_time = average_waiting_time
        self.average_turnaround_time = average_turnaround_time
        self.average_response_time = average_response_time
        # update processes
        self.processes = processes

    def save_result_simulation(self):
        """
        Save result of simulation to results/algorithmname.csv
        :param max_arrival_time: maximum number for random number of arrival time
        :param path: path to save csv file
        :param size: number of processes
        :return: bool
        """
        if not self.cpu_total_time > 0:
            print("you have to run an algorithm then save it")
            return

        self.processes.sort(key=lambda p: p.pid)
        data = []
        columns = [
            # process information
            'pid', 'arrival_time', 'priority', 'burst_time', 'waiting_time', 'turnaround_time', 'response_time',
            'start_time', 'end_time',
            # simulation information
            'total_process', 'run_time', 'cpu_total_time', 'cpu_run_time', 'cpu_utilization', 'throughput',
            'average_waiting_time', 'average_turnaround_time', 'average_response_time'
        ]
        # save data as lists of lists then create dataframe. e.g [ [pid1, arrival1], [pid2, arrival2]]
        for process in self.processes:
            data.append([
                process.pid,
                process.arrival_time,
                process.priority,
                process.burst_time,
                process.waiting_time,
                process.turnaround_time,
                process.response_time,
                process.start_time,
                process.end_time,
            ])

        # insert simulation information to just first row
        data[0].extend([
            self.total_process,
            self.run_time,
            self.cpu_total_time,
            self.cpu_run_time,
            self.cpu_utilization,
            self.throughput,
            self.average_waiting_time,
            self.average_turnaround_time,
            self.average_response_time
        ])
        df = pd.DataFrame(data, columns=columns)

        # handle path in linux and windows
        folder_path = Path("results/")
        df.to_csv(path_or_buf=folder_path / f"{self.algorithm}.csv", index=False)

        return True

    def analyze_algorithms(self):

        # handle path in linux and windows
        folder_path = Path("results/")
        columns = [
            'cpu_total_time', 'average_waiting_time', 'average_turnaround_time', 'average_response_time'
        ]
        algorithms_data = []
        exists_algorithms = []
        for algo in self.algorithms_list:
            try:
                df = pd.read_csv(folder_path / f"{self.algorithm}.csv", usecols=columns)
                algorithms_data.append([
                    algo,  # algorithm name
                    df['cpu_total_time'][0],
                    df['average_waiting_time'][0],
                    df['average_turnaround_time'][0],
                    df['average_response_time'][0],
                ])
                exists_algorithms.append(algo)
            except FileNotFoundError:
                pass

        if algorithms_data is None:
            raise Exception("You have to run one algorithm at least")

        columns.insert(0, 'name')
        algorithms_df = pd.DataFrame(algorithms_data, columns=columns, index=exists_algorithms)
        algorithms_df.to_csv(folder_path / "results.csv", index=False)

        # create subpot
        subplot = algorithms_df.plot(kind='bar')
        subplot.set_xlabel('algorithm name')
        subplot.set_ylabel('Time')
        subplot.set_title(f"analyze algorithms")
        subplot.legend()

        subplot.figure.set_size_inches(20.5, 15.5)
        # Set the figure title
        subplot.figure.canvas.manager.set_window_title(f"analyze {self.total_process} algorithms")
        subplot.figure.show()
        subplot.figure.savefig(folder_path / "result")

    def plot_algorithm_result(self):

        # handle path in linux and windows
        folder_path = Path("results/")
        try:
            df = pd.read_csv(folder_path / f"{self.algorithm}.csv")
        except FileNotFoundError:
            raise Exception("You should have run algorithm first")

        # set data
        try:
            self.run_time = df['run_time'][0]
            self.cpu_total_time = df['cpu_total_time'][0]
            self.cpu_run_time = df['cpu_run_time'][0]
            self.cpu_utilization = df['cpu_utilization'][0]
            self.throughput = df['throughput'][0]
            self.average_waiting_time = df['average_waiting_time'][0]
            self.average_turnaround_time = df['average_turnaround_time'][0]
            self.average_response_time = df['average_response_time'][0]
        except:
            pass

        df = df[['burst_time', 'arrival_time', 'priority', 'waiting_time', 'turnaround_time', 'response_time']]

        # get compressed dataframe for showing in chart
        # subplot settings based on priority
        priority_df = self._compress_df_rows(df, 'priority')
        priority_subplot = priority_df.plot(
            kind='bar',
            xlabel="Priority",
            ylabel="Time",
            title=self.algorithm
        )
        priority_subplot.figure.set_size_inches(30, 15)

        # subplot settings based on burst time
        burst_df = self._compress_df_rows(df, 'burst_time')
        burst_subplot = burst_df.plot(
            kind='bar',
            xlabel="Burst time",
            ylabel="Time",
            title=self.algorithm
        )
        burst_subplot.figure.set_size_inches(30, 15)

        # subplot settings based on arrival time
        arrival_df = self._compress_df_rows(df, 'arrival_time')
        arrival_subplot = arrival_df.plot(
            kind='bar',
            xlabel="Arrival time",
            ylabel="Time",
            title=self.algorithm
        )
        arrival_subplot.figure.set_size_inches(30, 15)

        fig_text = (
                'Simulation time: %.10f s\n'
                'CPU total time: %.0f s\n'
                'CPU run time: %.0f s\n'
                'CPU utilization: %.6f%%\n'
                'Throughput: %.6f\n'
                'Average waiting time: %.2f\n'
                'Average turnaround time: %.2f\n'
                'Average response time: %.2f' % (
                    self.run_time,
                    self.cpu_total_time,
                    self.cpu_run_time,
                    (self.cpu_utilization * 100),
                    self.throughput,
                    self.average_waiting_time,
                    self.average_turnaround_time,
                    self.average_response_time
                )
        )

        # add text to subplots
        priority_subplot.figure.text(
            0.5, 0.25,
            fig_text,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 50}
        )
        burst_subplot.figure.text(
            0.5, 0.25,
            fig_text,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 50}
        )
        arrival_subplot.figure.text(
            0.5, 0.25,
            fig_text,
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 50}
        )

        # show and save
        priority_subplot.figure.show()
        burst_subplot.figure.show()
        arrival_subplot.figure.show()

        # handle path in linux and windows
        fig_folder_path = Path("results/charts/")
        priority_subplot.figure.savefig(fig_folder_path / f'priority_{self.algorithm}')
        burst_subplot.figure.savefig(fig_folder_path / f'burst_{self.algorithm}')
        arrival_subplot.figure.savefig(fig_folder_path / f'arrival_{self.algorithm}')

    def json_export(self):
        return {
            "processes": self.processes,
            "total_process": self.total_process,
            "run_time": self.run_time,
            "cpu_total_time": self.cpu_total_time,
            "cpu_run_time": self.cpu_run_time,
            "throughput": self.throughput,
            "cpu_utilization": self.cpu_utilization,
            "average_waiting_time": self.average_waiting_time,
            "average_turnaround_time": self.average_turnaround_time,
            "average_response_time": self.average_response_time
        }

    def __str__(self):
        return (
            'Total processes: %.0f \n'
            'Simulation time: %.10f s\n'
            'CPU total time: %.0f \n'
            'CPU run time: %.0f s\n'
            'CPU utilization: %.6f%%\n'
            'Throughput: %.6f\n'
            'Average waiting time: %.2f\n'
            'Average turnaround time: %.2f\n'
            'Average response time: %.2f' % (
                self.total_process,
                self.run_time,
                self.cpu_total_time,
                self.cpu_run_time,
                (self.cpu_utilization * 100),
                self.throughput,
                self.average_waiting_time,
                self.average_turnaround_time,
                self.average_response_time
            )
        )


if __name__ == '__main__':
    simulation_graphic.run()
    # algorithm = "NonPreemptivePriority"
    # simulate = Simulator(algorithm)
    # for al in ["NonPreemptivePriority", "PreemptivePriority"]:
    #     s = Simulator(al)
    #     s.read_processes_data("data.csv")
    #     s.run()
    #     print(s.__str__())
    #     s.save_result_simulation()

    # simulate.analyze_algorithms()
    # simulate.read_processes_data()
    # simulate.run()
    # print(simulate.__str__())
    # simulate.save_result_simulation()
    # simulate.plot_algorithm_result()
