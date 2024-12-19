from .intersection_entry import IntersectionEntry

class Intersection:
    def __init__(self, car_arrival_rates, car_exit_rates, green_durations, yellow_duration):
        self.entries = [IntersectionEntry(rate, exit_rate, green, yellow_duration, i) for i, (rate, exit_rate, green) in enumerate(zip(car_arrival_rates, car_exit_rates, green_durations))]

        self.total_waiting_time = 0
        self.total_cars = 0
        for entry in self.entries:
            entry.intersection = self

    def process_all_entries(self, current_time):
        for entry in self.entries:
            entry.add_car(current_time)
            entry.process_cars(current_time)
            entry.update_phase()
