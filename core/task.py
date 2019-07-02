# Import built-in modules
import uuid
from pubsub import pub

# Import project modules
from core.task_segment import TaskSegment
from constants import *


def id_generator():
    return uuid.uuid1()


class Task:
    task_name = ''
    task_id = 0
    task_segments = []
    start_day = 0
    predecessors = []
    last_unmerged_segments = []

    def __init__(self):
        self.task_name = 'Unnamed Task'
        self.task_id = id_generator()
        ts1 = TaskSegment(self.start_day, 1)
        self.task_segments = [ts1]

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

    def get_finish(self):
        return self.start_day + self.get_virtual_duration() - 1

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
        """
        Set the total duration for the task.
        This is different from virtual duration.
        :param d: The total duration for the task.
        :return:
        """
        # Get the total duration fo the task
        total_duration = self.get_duration()

        # Get the last task segment from the list
        segment_n = self.task_segments[len(self.task_segments) - 1]

        # Difference between new duration and the existing
        diff = total_duration - d

        if diff <= 0:
            # New duration is longer than the previous
            # Add the difference to the last segment
            self.task_segments[len(self.task_segments) - 1].duration += abs(diff)
            return True
        else:
            # New duration is shorter
            if d < segment_n.duration:
                segment_n.duration -= diff
                return True
            else:
                return False, 'Task segments length shall be corrected before applying the ' \
                              'change in the total duration.'

    def set_start_day(self, s):
        """
        Change the default start day of the task and recursively update
        each task segment's start day.
        :param s: Start day (int)
        :return:
        """
        s = int(s)
        self.start_day = s

        # Adjust all start of task segments
        old_start = self.task_segments[0].start
        diff = s - old_start

        for ts in self.task_segments:
            ts.start += diff
        # pub.sendMessage(EVENT_PROJECT_UPDATED)

    def set_predecessors(self, task_indices_list):
        """
        Set the upstream task. The one it depends on to finish.
        :param task_indices_list: The list of task indices to be set as predecessor
        :return:
        """
        self.predecessors = task_indices_list

    def split_task(self, task_segment, left):
        """
        Cut a task part into two.
        :param task_segment: The task segment to be cut (e.g. is a task is already splitted into two and
            the second segment is the one to be split, use task_segment[1])
        :param left: The duration of the left part of the split.
        :return:
        """
        if not task_segment in self.task_segments:
            return
        total_duration = task_segment.duration
        start = task_segment.start

        start2 = start + left + 1

        # Check instance
        if not isinstance(task_segment, TaskSegment):
            return False, 'task_segment given is not an instance of TaskSegment class.'

        # Check the task segment duration
        if left >= total_duration:
            return False, 'The split duration of one part is greater than or not applicable to the task segment.'

        # Create two task segments
        ts1 = TaskSegment(start, left)
        ts2 = TaskSegment(start2, total_duration - left)

        # Replace the old task segment on the list
        location = self.task_segments.index(task_segment)
        self.task_segments[location:location+1] = ts1, ts2
        return True, (ts1, ts2)

    def undo_split_task(self, ts, ts1, ts2):
        if not ts1 in self.task_segments:
            return
        if not ts2 in self.task_segments:
            return
        insert_index = self.task_segments.index(ts1)
        self.task_segments.insert(insert_index, ts)
        self.task_segments.remove(ts1)
        self.task_segments.remove(ts2)
        return True, ts

    def merge_task_segments(self):
        import copy

        if len(self.task_segments) == 1:
            # Nothing to merge
            return False, 'Nothing to merge.'

        duration = self.get_duration()

        if len(self.last_unmerged_segments) == 0:
            for segment in self.task_segments:
                self.last_unmerged_segments.append(copy.copy(segment))

        for index, ts in enumerate(self.task_segments):
            if index != 0:
                self.task_segments.remove(ts)
                del ts

        self.task_segments[0].duration = duration

        return [True]

    def un_merge_task_segments(self):
        import copy

        for ts in self.task_segments:
            self.task_segments.remove(ts)
            del ts
        for segment in self.last_unmerged_segments:
            self.task_segments.append(copy.copy(segment))
