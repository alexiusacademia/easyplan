# Import built-in modules
import uuid

# Import project modules
from core.task_segment import TaskSegment


def id_generator():
    return uuid.uuid1()


class Task:
    task_name = ''
    task_id = 0
    task_segments = []
    start_day = 0
    upstream = None

    def __init__(self):
        self.task_name = 'Unnamed Task'
        self.task_id = id_generator()
        ts1 = TaskSegment(0, 1)
        self.task_segments.append(ts1)

    def rename(self, new_name):
        self.task_name = new_name

    def get_duration(self):
        """
        Get the duration by getting all the duration of each task segment in a task.
        :return:
        """
        total_duration = 0
        for ts in self.task_segments:
            if isinstance(ts, TaskSegment):
                total_duration += ts.duration
        return total_duration

    def get_virtual_duration(self):
        """
        Virtual duration is the total duration of a task.
        This will not be equal to the actual task duration if there is a splitting done in the task.
        :return:
        """
        virtual = 0

        # Get the first and last segment
        segment_1 = self.task_segments[0]
        segment_n = self.task_segments[len(self.task_segments) - 1]

        if isinstance(segment_1, TaskSegment) and isinstance(segment_n, TaskSegment):
            virtual = segment_n.start + segment_n.duration - segment_1.start
        return virtual

    def set_duration(self, d):
        # self.duration = d
        # Get the total duration fo the task
        total_duration = 0
        for ts in self.task_segments:
            if isinstance(ts, TaskSegment):
                total_duration += ts.duration

        # Get the last task segment from the list
        last_task_segment = TaskSegment(self.task_segments[len(self.task_segments) - 1])
        last_task_segment.duration

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
