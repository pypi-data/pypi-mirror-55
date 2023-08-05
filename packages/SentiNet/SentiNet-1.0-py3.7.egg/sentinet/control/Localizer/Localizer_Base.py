from multiprocessing import Pipe
from abc import ABC, abstractmethod
from sentinet.curmt import KermitControlModule
import numpy as np


class LocalizerBase(ABC):
	def __init__(self, pipe, sensors):
		self.pipe = pipe
		self.sensors = sensors
		self.position = np.full((3,1),None)
		self.velocity = np.full((3,1),None)
		self.ang_position = np.full((3,1),None)
		self.ang_velocity = np.full((3,1),None)

		for sensor in self.sensors.values():
			sensor.start_sensor()

	def pipe_value(self,value): #helper function to send value to state machine
		self.pipe.send(value)

	def end_localizer(self):
		for sensor in self.sensors.values():
			sensor.quit_sensor()

	@abstractmethod
	def filter(self):
		pass

	@abstractmethod
	def dynamics_model(self):
		pass

class SensorBase(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def start_sensor(self):
		pass

	@abstractmethod
	def quit_sensor(self):
		pass
		
	def get_data(self):
		return self.data

	@abstractmethod
	def callback(self):
		pass

	@abstractmethod
	def sensor_model(self):
		pass
