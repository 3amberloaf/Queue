import random

# Parameters
D = 10000  # Duration of the simulation
A = 2     # Average arrival rate of new passenger every A minutes
S = 10   # Average service rate in minutes
num_service_stations = 5
max_queue_length = 0
total_waiting_time = 0

# Initialize queues
queue = []  # Single queue for all service stations
service_stations = [0] * num_service_stations  # stations busy time

# Simulation loop
for time in range(D):
    # Generate random arrivals and service times
    if random.random() < (1 / A):
        arrival_time = time
        service_time = random.expovariate(1 / S)
        queue.append((arrival_time, service_time))
    
    # Check and update service stations
    for i in range(num_service_stations):
        if service_stations[i] == 0 and queue: # Checks if cu
            arrival_time, service_time = queue.pop(0) # Pop the first passenger off the queue if service station is available
            waiting_time = time - arrival_time
            total_waiting_time += waiting_time
            service_stations[i] = service_time
        
        if service_stations[i] > 0:
            service_stations[i] -= 1
    
    # Update maximum queue length
    max_queue_length = max(max_queue_length, len(queue))

# Calculate metrics
avg_waiting_time = total_waiting_time / (D * num_service_stations)
max_waiting_time = max([time[0] for time in queue]) if queue else 0

# Display results
print("Simulation Duration:", D)
print("Maximum Queue Length:", max_queue_length)
print("Average Waiting Time:", avg_waiting_time)
print("Maximum Waiting Time:", max_waiting_time)
