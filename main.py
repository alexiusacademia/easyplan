import core.task as task
from core.project import Project

t = task.Task()
t.task_name = 'Clearing'

p = Project()
p.add_task(t)

for task in p.tasks:
    print(task.task_id, task.task_name)