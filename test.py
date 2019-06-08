import core.task as task
from core.task_segment import TaskSegment
from core.project import Project

t = task.Task()
t.task_name = 'Clearing'
t.task_segments[0].duration = 20

for ts in t.task_segments:
    if isinstance(ts, TaskSegment):
        print(ts.start, ts.duration)

print('Duration of Clearing is: ' + str(t.get_duration()))
print('Virtual Duration of Clearing is: ' + str(t.get_virtual_duration()))

print('')

p = Project()
p.add_task(t)

p.tasks[0].set_duration(50)

clearing = p.tasks[0]
clearing1 = clearing.task_segments[0]

clearing.split_task(clearing1, 10)

clearing.split_task(clearing.task_segments[1], 30)

print(clearing.set_duration(40))

for t in p.tasks:
    print('---')
    for _ts in t.task_segments:
        print(str(_ts.start) + " - " + str(_ts.duration))
