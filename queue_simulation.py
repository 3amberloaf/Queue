import random
from collections import deque

num_stations = 5
arrival_rate = 1.5 # average arrival rate of a new passenger in minutes
duration = 50 # duration of the simultion in minutes
policies = ["single_queue", "random_queue", "round_robin", "shortest_queue" ]

# Represents arriving passenger
class Passenger:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time # Stores arrival  time for the passenger
        self.service_time = random.uniform(7.5, 10)  # Random service time between 7.5 and 10 minutes
        self.start_service_time = None # later will store the time when service starts for passengers

# Represents 5 Service Stations
class ServiceStation:
    def __init__(self):
        self.queue = deque() # initializes queue for passengers
        self.busy = False  # Keeps track if the station is occupied
        self.total_service_time = 0 # keeps track of total service time
        self.current_passenger = None # keeps track of current passenger
        self.max_queue_length = 0 
        self.waiting_times = [] # store waiting times of passengers

# Simulate queues
class QueueSimulation:
    def __init__(self, num_stations, arrival_rate, duration):
        self.num_stations = num_stations
        self.arrival_rate = arrival_rate
        self.duration = duration
        self.effective_duration = duration
        self.max_queue_length = 0
        self.stations = [ServiceStation() for _ in range(num_stations)] # creates 5 service stations
        self.time = 0 
        self.current_station = 0  # For round robin policy
        self.global_queue = deque()  # For single queue system
        self.total_passengers = []  # Keep track of all passengers
        self.policy = None # initializes policy attribute
    
    def run_simulation(self, policy):
        self.policy = policy  # chooses specific policy for this run
        self.reset_simulation()  # Reset simulation state for the new run
        while self.time < self.duration or self.any_passengers_remaining(): # while people are arriving or if any passengers remaining
            if self.time < self.duration:
                self.handle_arrivals() # checks if a new passenger arrived based on the arrival rate
            self.handle_departures() # checks to see if the passengers service is complete
            self.update_max_queue_length() 
            self.time += 1 # moves the simulation forward
        self.effective_duration = self.time 
        self.calculate_results()

    def update_max_queue_length(self):
        if self.policy == "single_queue":
            # Update only for the global queue in case of single_queue policy
            if len(self.global_queue) > self.max_queue_length:
                self.max_queue_length = len(self.global_queue)
        else:
            # Update for each station's queue
            for station in self.stations:
                if len(station.queue) > station.max_queue_length:
                    station.max_queue_length = len(station.queue)
    
    def any_passengers_remaining(self):
        stations_busy = any(station.busy for station in self.stations) # Check if any station is busy or if there are passengers in queues
        queues_not_empty = any(len(station.queue) > 0 for station in self.stations) or len(self.global_queue) > 0
        return stations_busy or queues_not_empty
    
    def reset_simulation(self):
        # Reset simulation state to initial values
        self.time = 0
        self.current_station = 0
        self.global_queue = deque()
        self.stations = [ServiceStation() for _ in range(self.num_stations)]
        self.total_passengers = []
        self.max_queue_length = 0 
        for station in self.stations:  # Reset each station's max queue length
            station.max_queue_length = 0
            station.waiting_times = []

    def handle_arrivals(self):
        if random.uniform(0, 1) < self.arrival_rate: 
            new_passenger = Passenger(self.time) # creates new passenger with arrival time 
            self.total_passengers.append(new_passenger)  # Track all passengers
            if self.policy == "single_queue":
                self.global_queue.append(new_passenger) # if the policy is a single queue then just add the new passenger
            else:
                self.select_station().queue.append(new_passenger) # otherwise add passenger to other queue based on policy
                
    def select_station(self):
        if self.policy == "round_robin":
            station = self.stations[self.current_station] # sets station variable to the current station
            self.current_station = (self.current_station + 1) % self.num_stations # makes sure it stays within the range of available stations
            return station
        elif self.policy == "shortest_queue":
            return min(self.stations, key=lambda x: len(x.queue)) # finds the shortest length of each stations queue
        elif self.policy == "random_queue":
            return random.choice(self.stations) # randomly chooses a station 

    def handle_departures(self):
        single_queue = self.policy == "single_queue"
        for station in self.stations:  # iterates through each station
            if station.busy and station.current_passenger:  # if the station is busy and has a current passenger
                # checks if passenger's service time finished
                if self.time - station.current_passenger.start_service_time >= station.current_passenger.service_time:
                    station.busy = False  # marks station as not busy
                    # updates total service time to include time spent servicing passenger
                    station.total_service_time += self.time - station.current_passenger.start_service_time
                    station.current_passenger = None  # removes passenger
            if not station.busy:
                next_passenger = None
                if single_queue and self.global_queue:  # checks if passengers are in single queue
                    next_passenger = self.global_queue.popleft()  # removes next passenger from global queue
                elif not single_queue and station.queue:
                    next_passenger = station.queue.popleft()  # removes next passenger from station queue

                if next_passenger:
                    # Calculate waiting time as the current time minus the passenger's arrival time
                    waiting_time = self.time - next_passenger.arrival_time
                    station.waiting_times.append(waiting_time)  # Record waiting time for this passenger

                    # Begin servicing the next passenger
                    station.current_passenger = next_passenger
                    station.busy = True
                    station.current_passenger.start_service_time = self.time  # sets the service time to current time


    def calculate_results(self):
        if len(self.total_passengers) > 0:
            total_waiting_time = sum((p.start_service_time - p.arrival_time) for p in self.total_passengers if p.start_service_time is not None) # each passenger's waiting time is the difference between start service and arrival
            avg_waiting_time = total_waiting_time / len([p for p in self.total_passengers if p.start_service_time is not None]) # only includes passengers who have started service
            if any(p.start_service_time is not None for p in self.total_passengers):
                max_waiting_time = max((p.start_service_time - p.arrival_time) for p in self.total_passengers if p.start_service_time is not None) # finds the longest waiting time
            else:
                max_waiting_time = 0
        else:
            avg_waiting_time = 0
            max_waiting_time = 0
            total_waiting_time = 0
            
       
        print(f"\nSimulation Duration in Minutes: {self.effective_duration}")
        if self.policy == "single_queue":
            print("Maximum Global Queue Length:", self.max_queue_length, "passengers")
        else:
            print("Maximum Queue Lengths for Each Station:")
            for i, station in enumerate(self.stations):
                print(f"Station {i + 1}: {station.max_queue_length}",  "passengers")
        
        print(f"\nAverage Waiting Time:")
        for i, station in enumerate(self.stations):
            avg_waiting_time = sum(station.waiting_times) / len(station.waiting_times)
            print(f"Station {i + 1}: {avg_waiting_time:.2f} minutes")
            
        print(f"\nMaximum Waiting Time:")
        for i, station in enumerate(self.stations):
            max_waiting_time = max(station.waiting_times)
            print(f"Station {i + 1}: {max_waiting_time:.2f} minutes")
        
        print(f"\nService Station Occupancy:")
        for i, station in enumerate(self.stations):
            occupancy_rate = (station.total_service_time / self.effective_duration) * 100 if station.total_service_time else 0
            print(f"Station {i + 1}: {occupancy_rate:.2f}%")


simulation = QueueSimulation(num_stations, arrival_rate, duration)

for policy in policies:
    print(f"\nRunning simulation with {policy} policy")
    simulation.run_simulation(policy)