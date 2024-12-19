from .intersection import Intersection

def simulate_traffic(car_arrival_rates, green_light_durations, yellow_light_duration, car_exit_rates, simulation_time):
    intersection = Intersection(car_arrival_rates, car_exit_rates, green_light_durations, yellow_light_duration)
    current_time = 0
    

    while current_time < simulation_time:
        intersection.process_all_entries(current_time)
        current_time += 1

    # Calculate average waiting time
    return intersection