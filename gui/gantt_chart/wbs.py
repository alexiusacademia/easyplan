import wx.grid as gridlib


class WBS(gridlib.Grid):
    project = None

    def __init__(self, parent, project):
        gridlib.Grid.__init__(self, parent, -1)

        self.project = project

        self.CreateGrid(0, 4)
        # self.SetTable(table, True)
        self.SetRowLabelSize(30)
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

    def populate(self):
        num_rows = self.GetNumberRows()
        index = 0
        for task in self.project.tasks:
            if num_rows < index+1:
                self.AppendRows()
            self.SetCellValue(index, 0, str(task.task_name))
            self.SetCellValue(index, 1, str(task.start_day))
            self.SetCellValue(index, 2, str(task.get_duration()))
            self.SetCellValue(index, 3, str(task.predecessor))

            index += 1
