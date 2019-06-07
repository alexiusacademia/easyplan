import uuid


def id_generator():
    return uuid.uuid1()


class Task:
    task_name = ''
    task_id = 0
    duration = 0
    task_segments = []
    start_day = 0
    upstream = None

    def __init__(self):
        self.task_name = 'Unnamed Task'
        self.task_id = id_generator()

    def rename(self, new_name):
        self.task_name = new_name

    def set_duration(self, d):
        self.duration = d

    def set_start_day(self, s):
        self.start_day = s

    def set_upstream(self, task):
        """
        Set the upstream task. The one it depends on to finish.
        :param task:
        :return:
        """
        if isinstance(task, Task):
            self.upstream = task
            return True, 'Upstream set.'
        else:
            return False, 'Task must be an instance of task.'

    def split_task(self, task_part, left):
        """
        Cut a task part into two.
        :param task_part: The task segment to be cut (e.g. is a task is already splitted into two and
            the second segment is the one to be split, use task_segment[1])
        :param left: The duration of the left part of the split.
        :return:
        """
        pass