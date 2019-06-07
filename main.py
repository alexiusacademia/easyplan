import core.task as task
from core.task_segment import TaskSegment
from core.project import Project

t = task.Task()
t.task_name = 'Clearing'
for ts in t.task_segments:
    if isinstance(ts, TaskSegment):
        print(ts.start, ts.duration)

print('Duration of Clearing is: ' + str(t.get_duration()))

p = Project()
p.add_task(t)

for task in p.tasks:
    print(task.task_id, task.task_name)