import uuid


def id_generator():
    return uuid.uuid1()


class Task:
    task_name = ''
    task_id = 0
    duration = 0
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
        if isinstance(task, self):
            self.upstream = task
            return True, 'Upstream set.'
        else:
            return False, 'Task must be an instance of task.'
