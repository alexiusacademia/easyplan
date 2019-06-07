# Import built-in modules
import uuid

# Import project modules
from core.task_segment import TaskSegment


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

    def split_task(self, task_segment, left):
        """
        Cut a task part into two.
        :param task_segment: The task segment to be cut (e.g. is a task is already splitted into two and
            the second segment is the one to be split, use task_segment[1])
        :param left: The duration of the left part of the split.
        :return:
        """
        total_duration = task_segment.duration
        start = task_segment.start

        # Check instance
        if not isinstance(task_segment, TaskSegment):
            return False, 'task_segment given is not an instance of TaskSegment class.'

        # Check the task segment duration
        if left >= total_duration:
            return False, 'The split duration of one part is greater than or not applicable to the task segment.'

        # Create two task segments
        ts1 = TaskSegment(start, left)
        ts2 = TaskSegment(left, total_duration - left)

        # Replace the old task segment on the list
        location = self.task_segments.index(task_segment)
        self.task_segments[location:location+1] = ts1, ts2
