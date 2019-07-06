import wx.grid as gridlib
import wx
from pubsub import pub

from constants import *
from core.task import Task


class Cols(enumerate):
    TASK_NAME = 0
    START_DAY = 1
    DURATION = 2
    FINISH_DAY = 3
    PREDECESSORS = 4
    RESOURCES = 5


class WBS(gridlib.Grid):
    project = None

    def __init__(self, parent, project, controller):
        gridlib.Grid.__init__(self, parent, -1)

        self.project = project
        self.controller = controller

        self.CreateGrid(0, 6)

        self.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.SetRowLabelSize(30)
        self.SetColLabelSize(40)
        # self.SetMargins(0, 0)

        for i in range(100):
            self.SetRowLabelValue(i, str(i + 1))

        self.SetColLabelValue(Cols.TASK_NAME, 'Task Name')
        self.SetColLabelValue(Cols.START_DAY, 'Start')
        self.SetColLabelValue(Cols.DURATION, 'Duration')
        self.SetColLabelValue(Cols.FINISH_DAY, 'Finish')
        self.SetColLabelValue(Cols.PREDECESSORS, 'Predecessors')
        self.SetColLabelValue(Cols.RESOURCES, 'Resources')

        # self.AutoSizeColumns(True)
        self.SetColSize(Cols.TASK_NAME, 200)
        self.Layout()

        self.create_bindings()

    def create_bindings(self):
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.on_row_selected)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.on_cell_edit_complete)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGING, self.on_cell_selected)

        pub.subscribe(self.on_project_updated, EVENT_PROJECT_UPDATED)
        pub.subscribe(self.on_task_moving, EVENT_BAR_SEGMENT_MOVING)
        pub.subscribe(self.on_task_start_updated, EVENT_TASK_START_UPDATED)
        pub.subscribe(self.on_duration_updated, EVENT_TASK_DURATION_UPDATED)

    def on_task_moving(self, task, task_segment, task_start):
        index = self.project.tasks.index(task)
        index_of_ts = task.task_segments.index(task_segment)
        if task_start is not None and index_of_ts == 0:
            # self.SetCellValue(index, Cols.START_DAY, str(task_start))
            self.populate()

    def on_hide(self, event):
        print('Hide')

    def populate(self):
        """
        Populate the grid with the data from the project object.
        :return:
        """
        self.delete_all_rows()
        if self.project is not None:
            num_rows = self.GetNumberRows()
            index = 0
            for task in self.project.tasks:
                if num_rows < index+1:
                    self.AppendRows()
                self.SetCellValue(index, Cols.TASK_NAME, str(task.task_name))
                self.SetCellValue(index, Cols.START_DAY, str(task.start_day))
                self.SetCellValue(index, Cols.DURATION, str(task.get_duration()))
                self.SetCellValue(index, Cols.FINISH_DAY, str(task.get_finish()))

                self.SetReadOnly(index, Cols.FINISH_DAY, True)

                task_predecessors_temp = task.predecessors

                # Convert to indices
                task_list = []
                for tpt in task_predecessors_temp:
                    task_list.append(self.project.tasks.index(tpt) + 1)

                # Convert list to comma delimited string
                task_predecessors_str = str(task_list)
                task_predecessors_str = task_predecessors_str.replace('[', '')
                task_predecessors_str = task_predecessors_str.replace(']', '')

                self.SetCellValue(index, Cols.PREDECESSORS, task_predecessors_str)

                self.SetCellValue(index, Cols.RESOURCES, '')

                self.SetRowSize(index, WBS_ROW_HEIGHT)

                index += 1

    def delete_all_rows(self):
        """
        Just delete all the rows.
        :return:
        """
        if self.GetNumberRows() > 0:
            self.DeleteRows(0, self.GetNumberRows())

    def on_row_selected(self, event):
        """
        Event when a row is selected.
        :param event:
        :return:
        """
        if isinstance(event, gridlib.GridEvent):
            index = event.GetRow()
            self.SelectRow(index)
            self.project.selected_task_index = index

    def on_cell_edit_complete(self, event):
        """
        Called when cell editing is complete.
        :param event:
        :return:
        """
        if isinstance(event, gridlib.GridEvent):
            cell = event.GetRow(), event.GetCol()
            self.update_project(cell[0], cell[1], event.GetString())

    def update_project(self, index, col, old):
        """
        Called by the handler of end of cell editing.
        :param index: Row index
        :param col: Column index
        :param old: Old cell value
        """
        tasks = self.project.tasks
        task = tasks[index]
        cell = index, col
        value = self.GetCellValue(cell)
        # Task name
        if col == Cols.TASK_NAME:
            task.task_name = value
        # Task start day
        elif col == Cols.START_DAY:
            if value.isdigit():
                task.set_start_day(int(value))
                self.project.update_start_days()
                pub.sendMessage(EVENT_TASK_START_UPDATED, index=index, start=int(value))
            else:
                self.SetCellValue(cell, old)

        # Task duration
        elif col == Cols.DURATION:
            if value.isdigit():
                duration = int(value)
                task.set_duration(duration)

                pub.sendMessage(EVENT_TASK_DURATION_UPDATED)

        # Predecessor
        elif col == Cols.PREDECESSORS:
            # Value must be a single integer or a list of integers

            temp = value.replace(' ', '')
            temp = temp.split(',')
            predecessors = []
            if value == '':
                self.project.set_task_predecessors(task, predecessors)
                self.project.update_start_days()
                return

            for t in temp:
                if not t.isdigit():
                    self.SetCellValue(cell, old)
                    return
                else:
                    predecessors.append(self.project.tasks[int(t) - 1])

            self.project.set_task_predecessors(task, predecessors)

        self.project.update_start_days()

    def on_cell_selected(self, event):
        row_index = event.GetRow()
        task = self.project.tasks[row_index]
        self.project.selected_task = task
        self.project.selected_task_index = row_index

    def on_task_start_updated(self, index, start):
        self.SetCellValue((index, Cols.START_DAY), str(start))

        task: Task = self.project.tasks[index]
        self.SetCellValue((index, Cols.FINISH_DAY), str(task.get_finish()))

    def on_duration_updated(self):
        task: Task = self.project.selected_task
        index = self.project.tasks.index(task)
        self.SetCellValue((index, Cols.FINISH_DAY), str(task.get_finish()))

    def on_project_updated(self):
        self.populate()


def show_error(message, caption):
    wx.MessageBox(message, caption)


# TODO Indent
# TODO Outdent
# TODO ValueError
