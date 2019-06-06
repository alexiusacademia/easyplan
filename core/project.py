from enum import Enum


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
    _tasks = []

    # Set the time basis default to day. Meaning a whole day is just one count regardless of the length
    # of hours used in work.
    _time_basis = TimeBasis.DAY

    def __init__(self):
        pass

    def add_task(self, task):
        """
        Add a task to the project. The task start day will be on the first day by default and the
        user will have to move in to its appropriate location of by adding dependencies or dependents.
        :param task: A task object containing all the necessary information.
        :return:
        """
        self._tasks.append(task)

    def remove_task(self, task):
        """
        Remove a specific task.
        :param task:
        :return: Returns true if the task is successfully deleted.
        """
        try:
            self._tasks.remove(task)
            return True
        except ValueError:
            return False
