import unittest
from .config_loader import load_config  # Use relative import

from queue_simulation import Passenger, ServiceStation, QueueSimulation

class TestPassenger(unittest.TestCase):
    def test_passenger_creation(self):
        arrival_time = 5
        passenger = Passenger(arrival_time)
        self.assertEqual(passenger.arrival_time, 5)
        self.assertTrue(0.5 <= passenger.service_time <= 1.5)

class TestServiceStation(unittest.TestCase):
    def test_station_initialization(self):
        station = ServiceStation()
        self.assertFalse(station.busy)
        self.assertEqual(station.total_service_time, 0)
        self.assertIsNone(station.current_passenger)
        self.assertTrue(station.queue.empty())

class TestQueueSimulation(unittest.TestCase):
    def test_simulation_initialization(self):
        simulation = QueueSimulation(3, 0.1, 1000)
        self.assertEqual(len(simulation.stations), 3)
        self.assertEqual(simulation.arrival_rate, 0.1)
        self.assertEqual(simulation.duration, 1000)

    def test_handle_arrivals_single_queue(self):
        simulation = QueueSimulation(1, 1, 1)  # High arrival rate to ensure a passenger is added
        simulation.run_simulation("single_queue")
        self.assertFalse(simulation.global_queue.empty())

    def test_handle_departures_single_queue(self):
        simulation = QueueSimulation(1, 1, 1)
        simulation.run_simulation("single_queue")
        simulation.handle_departures()  # Run departures once to potentially clear the queue
        # This test might need to be more detailed, checking if a passenger was served

if __name__ == '__main__':
    unittest.main()
