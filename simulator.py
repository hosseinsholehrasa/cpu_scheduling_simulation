from datetime import datetime


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


