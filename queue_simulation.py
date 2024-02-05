import random
import queue

num_stations = 5
arrival_rate = 0.02
duration = 5
policies = ["single_queue", "round_robin", "shortest_queue", "random_queue"]
  

# Represents arriving passenger
class Passenger:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time # Stores arrival  time
        self.service_time = random.uniform(0.5, 1.5)  # Random service time between 0.5 and 1.5 minutes
        self.start_service_time = None

# Service Station class
class ServiceStation:
    def __init__(self):
        self.queue = queue.Queue() # initializes queue for passengers
        self.busy = False  # Keeps track if the station is occupied
        self.total_service_time = 0
        self.current_passenger = None

# Simulate queue
class QueueSimulation:
    def __init__(self, num_stations, arrival_rate, duration):
        self.num_stations = num_stations
        self.arrival_rate = arrival_rate
        self.duration = duration
        self.stations = [ServiceStation() for _ in range(num_stations)]
        self.time = 0
        self.current_station = 0  # For round robin policy
        self.global_queue = queue.Queue()  # For single queue system
        self.total_passengers = []  # Keep track of all passengers
        
    
    def run_simulation(self, policy):
        self.policy = policy  # Set policy for this run
        self.reset_simulation()  # Reset simulation state for the new run
        while self.time < self.duration:
            self.handle_arrivals()
            self.handle_departures()
            self.time += 1
        self.calculate_results()

    def reset_simulation(self):
        # Reset simulation state
        self.time = 0
        self.current_station = 0
        self.global_queue = queue.Queue()
        self.stations = [ServiceStation() for _ in range(self.num_stations)]
        self.total_passengers = []

    def handle_arrivals(self):
        if random.uniform(0, 1) < self.arrival_rate:
            new_passenger = Passenger(self.time)
            self.total_passengers.append(new_passenger)  # Track all passengers
            if self.policy == "single_queue":
                self.global_queue.put(new_passenger)
            else:
                station = self.select_station()
                station.queue.put(new_passenger)

    def select_station(self):
        if self.policy == "round_robin":
            station = self.stations[self.current_station]
            self.current_station = (self.current_station + 1) % self.num_stations
            return station
        elif self.policy == "shortest_queue":
            return min(self.stations, key=lambda x: x.queue.qsize())
        elif self.policy == "random_queue":
            return random.choice(self.stations)
        else:
            raise ValueError("Unknown policy")

    def handle_departures(self):
        if self.policy == "single_queue" and not self.global_queue.empty():
            for station in self.stations:
                if not station.busy:
                    station.current_passenger = self.global_queue.get()
                    station.busy = True
                    station.current_passenger.start_service_time = self.time
        for station in self.stations:
            if station.busy and station.current_passenger and self.time - station.current_passenger.start_service_time >= station.current_passenger.service_time:
                station.busy = False
                station.total_service_time += self.time - station.current_passenger.start_service_time
                station.current_passenger = None
            elif not station.busy and not station.queue.empty() and self.policy != "single_queue":
                station.current_passenger = station.queue.get()
                station.busy = True
                station.current_passenger.start_service_time = self.time

    def calculate_results(self):
        if len(self.total_passengers) > 0:
            total_waiting_time = sum((p.start_service_time - p.arrival_time) for p in self.total_passengers if p.start_service_time is not None)
            avg_waiting_time = total_waiting_time / len([p for p in self.total_passengers if p.start_service_time is not None])
            # Ensure there are passengers who have started service to calculate max waiting time
            if any(p.start_service_time is not None for p in self.total_passengers):
                max_waiting_time = max((p.start_service_time - p.arrival_time) for p in self.total_passengers if p.start_service_time is not None)
            else:
                max_waiting_time = 0
        else:
            avg_waiting_time = 0
            max_waiting_time = 0
            total_waiting_time = 0  # This may be redundant but is added for clarity
        
        max_queue_length = max([station.queue.qsize() for station in self.stations] + [self.global_queue.qsize()])

        print(f"\nSimulation Duration: {self.duration}")  # Use self.duration instead of self.time for clarity
        print(f"Policy: {self.policy}")
        print("Maximum Queue Length:", max_queue_length)
        print("Average Waiting Time:", avg_waiting_time)
        print("Maximum Waiting Time:", max_waiting_time)
        print("Total Waiting Time:", total_waiting_time)  # If you want to display this
        print("Service Station Occupancy:")
        for i, station in enumerate(self.stations):
            occupancy_rate = (station.total_service_time / self.duration) * 100 if station.total_service_time else 0
            print(f"Station {i + 1}: {occupancy_rate:.2f}%")

simulation = QueueSimulation(num_stations, arrival_rate, duration)

policies = ["single_queue", "round_robin", "shortest_queue", "random_queue"]
for policy in policies:
    print(f"\nRunning simulation with {policy} policy")
    simulation = QueueSimulation(num_stations, arrival_rate, duration)
    simulation.run_simulation(policy)