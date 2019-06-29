# Import built-in modules
from enum import Enum
import datetime
from pubsub import pub

# Import project modules
from . import task as tsk
from constants import *
from core.task import Task


class TimeBasis(Enum):
    TIME = 1
    DAY = 2


class Project:
    """
    Class Project to hold a project object.
    If the object is not yet initialized, all the controls and widgets that
      the gui used for a project must be disabled.
    A project object shall contain tasks, calendar, work time, statistics, project information,
      etc.
    """
    _initialized = False

    # List of task objects that will be implemented in the project.
    tasks = []

    # Set the time basis default to day. Meaning a whole day is just one count regardless of the length
    # of hours used in work.
    _time_basis = TimeBasis.DAY

    project_name = 'New Project'
    project_location = ''
    project_amount = ''
    selected_task_index = None
    selected_task = None
    selected_task_segment = None
    start_date = datetime.date.today()

    # Gantt Chart
    # -------------------------
    interval_major_axis = 7  # days

    def __init__(self):
        self._initialized = True

    def add_task(self, task):
        """
        Add a task to the project. The task start day will be on the first day by default and the
        user will have to move in to its appropriate location of by adding dependencies or dependents.
        :param task: A task object containing all the necessary information.
        :return:
        """
        if isinstance(task, tsk.Task):
            self.tasks.append(task)
            pub.sendMessage(EVENT_PROJECT_UPDATED)
            return True
        else:
            return False

    def insert_task(self, index, task):
        self.tasks.insert(index, task)
        pub.sendMessage(EVENT_PROJECT_UPDATED)

    def remove_task(self, task):
        """
        Remove a specific task.
        :param task:
        :return: Returns true if the task is successfully deleted.
        """
        try:
            if isinstance(task, tsk.Task):
                index = self.tasks.index(task)

                # Find all tasks that depend on this then remove the dependency
                for t in self.tasks:
                    if len(t.predecessors) > 0:
                        for pred in t.predecessors:
                            if pred == task:
                                t.predecessors.remove(task)

                self.tasks.remove(task)
                pub.sendMessage(EVENT_PROJECT_UPDATED)
                return True
            else:
                return False
        except ValueError:
            return False

    def update_successors(self):
        # Update all successors recursively
        for i in range(len(self.tasks)):
            for index, task in enumerate(self.tasks):
                if len(task.predecessors) > 0:
                    for pred in task.predecessors:
                        pred_end = pred.start_day + pred.get_virtual_duration()
                        if pred_end > task.start_day:
                            task.set_start_day(pred_end)

        pub.sendMessage(EVENT_PROJECT_UPDATED)

    def change_task_index(self, index, direction=-1):
        new_index = index + direction
        self.tasks.insert(new_index, self.tasks.pop(index))

        pub.sendMessage(EVENT_PROJECT_UPDATED)

    def move_task_segment(self, task, task_segment, start):
        task_segment.start = start

        # Get the task segment index from the task
        index_of_ts = task.task_segments.index(task_segment)

        if index_of_ts == 0:
            # Start of this segment represents start of the task
            task.set_start_day(start)
            task_start = start
        else:
            task_start = None

        # pub.sendMessage(EVENT_BAR_SEGMENT_MOVING, task=task, task_segment=task_segment, task_start=task_start)
        pub.sendMessage(EVENT_UPDATE_PREDECESSOR_LINES)

    def set_task_predecessors(self, task, task_indices_list):
        task.set_predecessors(task_indices_list)
        pub.sendMessage(EVENT_TASK_PREDECESSORS_UPDATED)

    def update_start_days(self):
        tasks = self.tasks

        for i, task in enumerate(tasks):
            num_predecessors = len(task.predecessors)
            if num_predecessors > 0:
                first_predecessor: Task = task.predecessors[0]
                max_end = first_predecessor.start_day + first_predecessor.get_virtual_duration()

                for pred in task.predecessors:
                    end = pred.start_day + pred.get_virtual_duration()
                    if end > max_end:
                        max_end = end

                if task.start_day < max_end:
                    task.set_start_day(max_end)

                    pub.sendMessage(EVENT_TASK_START_UPDATED, index=i, start=max_end)

    def get_project_duration(self):
        total_duration = 0
        for task in self.tasks:
            total_duration += task.get_virtual_duration()

        return total_duration
