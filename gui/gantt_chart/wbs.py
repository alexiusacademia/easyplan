import wx.grid as gridlib
import wx


class Cols(enumerate):
    TASK_NAME = 0
    START_DAY = 1
    DURATION = 2
    PREDECESSOR = 3


class WBS(gridlib.Grid):
    project = None

    def __init__(self, parent, project, controller):
        gridlib.Grid.__init__(self, parent, -1)

        self.project = project
        self.controller = controller

        self.CreateGrid(0, 4)
        # self.SetTable(table, True)
        self.SetRowLabelSize(30)
        self.SetColLabelSize(40)
        # self.SetMargins(0, 0)

        for i in range(100):
            self.SetRowLabelValue(i, str(i + 1))

        self.SetColLabelValue(0, 'Task Name')
        self.SetColLabelValue(1, 'Start Day')
        self.SetColLabelValue(2, 'Duration')
        self.SetColLabelValue(3, 'Predecessor')

        # self.AutoSizeColumns(True)
        self.SetColSize(0, 200)
        self.Layout()

        self.create_bindings()

    def create_bindings(self):
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.on_row_selected)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.on_cell_edit_complete)

    def on_hide(self, event):
        print('Hide')

    def populate(self):
        """
        Populate the grid with the data from the project object.
        :return:
        """
        self.delete_all_rows()
        num_rows = self.GetNumberRows()
        index = 0
        for task in self.project.tasks:
            if num_rows < index+1:
                self.AppendRows()
            self.SetCellValue(index, 0, str(task.task_name))
            self.SetCellValue(index, 1, str(task.start_day))
            self.SetCellValue(index, 2, str(task.get_duration()))
            self.SetCellValue(index, 3, str(task.predecessor))

            self.SetRowSize(index, 30)

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
            # self.controller.refresh()
            self.controller.right_pane.redraw()

    def update_project(self, index, col, old):
        """
        Called by the handler of end of cell editing.
        :param index: Row index
        :param col: Column index
        :param old: Old cell value
        """
        task = self.project.tasks[index]
        cell = index, col
        value = self.GetCellValue(cell)
        # Task name
        if col == 0:
            task.task_name = value
        # Task start day
        elif col == 1:
            if value.isdigit():
                # Now check if this is the first task,
                # if it is, make sure that it starts at first day (e.g. day 1)
                if index == 0 and int(value) != 1:
                    self.SetCellValue(cell, old)
                else:
                    task.set_start_day(value - 1)
        # Task duration
        elif col == 2:
            if value.isdigit():
                task.set_duration(int(value))
        # Predecessor
        elif col == 3:
            if value.isdigit():
                if int(value) == index+1:
                    self.SetCellValue(cell, old)
                elif int(value) > len(self.project.tasks):
                    self.SetCellValue(cell, old)
                else:
                    task.predecessor = int(value) - 1


def show_error(message, caption):
    wx.MessageBox(message, caption)


# TODO Indent
# TODO Outdent
# TODO ValueError
