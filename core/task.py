import uuid


def id_generator():
    return uuid.uuid1()


class Task:
    task_name = ''
    task_id = 0

    def __init__(self, name):
        """
        Constructor specifying the name of the task.
        :param name:
        """
        self.task_name = name
        self.task_id = id_generator()