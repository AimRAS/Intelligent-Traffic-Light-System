
import random
from .car import Car


class IntersectionEntry:
    def __init__(self, car_arrival_rate, car_exit_rate, green_duration, yellow_duration, index):
        self.cars = []
        self.car_arrival_rate = car_arrival_rate
        self.car_exit_rate = car_exit_rate
        self.green_duration = green_duration
        self.yellow_duration = yellow_duration
        self.red_duration = -1  # To be calculated
        self.current_phase = "red"  # Initial phase
        self.phase_timer = self.red_duration
        self.index = index
        self.cars_popped_per_time_step = []  # To store the number of cars popped at each time step
        self.phase_history = []  # To store the phase at each time step
        self.uneffective_phase_track = 0



    def add_car(self, current_time):
        if random.random() < self.car_arrival_rate:
            self.cars.append(Car(current_time, self.index))

    def process_cars(self, current_time):
        cars_popped_this_time_step = 0

        if self.current_phase == "green":
            for _ in range(int(self.car_exit_rate)):
                if self.cars:
                    car = self.cars.pop(0)
                    car.set_exit_time(current_time)
                    self.intersection.total_waiting_time += car.get_waiting_time()
                    self.intersection.total_cars += 1
                    cars_popped_this_time_step += 1
            # if cars_popped_this_time_step
        self.cars_popped_per_time_step.append(cars_popped_this_time_step)
        self.phase_history.append(self.current_phase)



    def update_phase(self):
        self.phase_timer -= 1
        if self.phase_timer <= 0:
            if self.current_phase == "red":
                # Check if all other entries are also red
                if all(entry.current_phase != "green" for entry in self.intersection.entries if entry != self):
                    self.current_phase = "green"
                    self.phase_timer = self.green_duration
            elif self.current_phase == "green":
                # Optimization for next green
                last_green_elements = self.cars_popped_per_time_step[-self.green_duration:]
                max_flow = max(last_green_elements)
                count_uneffitive = 0
                for element in self.cars_popped_per_time_step[::-1]: # Iterate from the end without reversing 
                    if element < 0.7* max_flow: 
                        count_uneffitive += 1 
                    else: 
                        break


                
                if count_uneffitive <= 1:
                    self.green_duration = self.green_duration + 2
                else:
                    self.green_duration = self.green_duration - count_uneffitive + 2


                # last_three_time_steps = self.cars_popped_per_time_step[-5:]
                # cond = 0.7 * self.car_exit_rate
                # if all(element < cond for element in last_three_time_steps):
                #     self.green_duration = self.green_duration - 2
                # elif all(element > cond for element in last_three_time_steps):
                #     self.green_duration = self.green_duration + 2

                self.current_phase = "yellow"
                self.phase_timer = self.yellow_duration
            elif self.current_phase == "yellow":
                self.current_phase = "red"
                # Calculate red duration based on other lights' green and yellow durations
                self.red_duration = sum([entry.green_duration + entry.yellow_duration for entry in self.intersection.entries if entry != self])
                # self.red_duration = max_green_yellow_time - self.green_duration - self.yellow_duration
                self.phase_timer = self.red_duration
