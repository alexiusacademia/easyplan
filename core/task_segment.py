class TaskSegment:
    start = 0
    duration = 0

    def __init__(self, st, dur):
        self.start = st
        self.duration = dur

    def move(self, start):
        self.start = start

    def get_finish(self):
        return self.start + self.duration - 1
