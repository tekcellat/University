class Queue:
    def __init__(self):
        self.size = 0
        self.data = []

    def add_request(self, t):
        self.data.append(t)
        self.size += 1

    def remove_request(self, t):
        if self.size > 0:
            self.size -= 1
            return t - self.data.pop(0)
        else:
            return 0
