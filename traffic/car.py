class Car:
    def __init__(self, entry_time, entry_index):
        self.entry_time = entry_time
        self.exit_time = None
        self.entry_index = entry_index

    def set_exit_time(self, exit_time):
        self.exit_time = exit_time

    def get_waiting_time(self):
        return self.exit_time - self.entry_time