from sentinet.control.Localizer.Localizer_Base import LocalizerBase, SensorBase
from threading import Lock
from sentinet.curmt import KermitControlModule
import numpy as np

# Some default variables for function calls.
turn_gain = 0.015
drive_gain = 0.015
time_step = 1.0


# Test basic class for operation for a localizer.
class DummyLocalizer(LocalizerBase):
	##
	# @brief Initializes the DummyLocalizer class. If no values are set, it will just set values to default.
	#
	# @param pipe The pathway the information is traveling through.
	# @param sensors The actual name of the sensor that the is sending information.
	def __init__(self, pipe, sensors):
		super().__init__(pipe, sensors)
		if None in self.position:
			self.position.fill(0.0)
		if None in self.velocity:
			self.velocity.fill(0.0)
		if None in self.ang_position:
			self.ang_position.fill(0.0)
		if None in self.ang_velocity:
			self.ang_velocity.fill(0.0)
		self.pipe_value([self.position, self.ang_position])
		self.run_localizer()
			
	# @brief Stores data for the localizer for passing to the pipe.
	def filter(self):
		# integrate sensor data forward
		for sensor_name, sensor in zip(self.sensors.keys(),self.sensors.values()):
			if sensor_name is 'DummySensor':
				cmd_vel = sensor.get_data()
				throttle = cmd_vel[0]
				turn_ratio = cmd_vel[1]
				self.velocity = np.array([np.cos(float(self.ang_position[0]))*throttle*drive_gain, np.sin(float(self.ang_position[0]))*throttle*drive_gain, 0])
				self.ang_velocity = np.array([np.pi*turn_ratio*turn_gain, 0, 0])
				self.position = self.position + np.array([self.velocity[0]*time_step, self.velocity[1]*time_step, self.velocity[2]*time_step])
				self.ang_position = self.ang_position + np.array([self.ang_velocity[0]*time_step, self.ang_velocity[1]*time_step, self.ang_velocity[2]*time_step])
		self.pipe_value([self.position, self.ang_position])

	def run_localizer(self):
		while True:
			try:
				if self.read_pipe() == 'fin':
					self.end_localizer()
					exit()
				else:
					self.filter()
			except KeyboardInterrupt:
				exit()
	
	def dynamics_model(self):
		return 0

# @brief Basic template for a sensor.
class DummySensor(SensorBase):
	# @brief Just initializes the content inside in the class.
	def __init__(self):
		self.data = [0,0]
		self.lock = Lock()
		self.ControlModule = KermitControlModule(requesting=True)
		self.ControlModule.set_data_callback(self.callback)

	def start_sensor(self):
		self.ControlModule.start_kermit()

	def quit_sensor(self):
		self.ControlModule.quit_kermit()
	
	# @brief Assignes content and information for the sensor storing the sensors infromation in itself. Protecting information by locking it	
	def callback(self, throttle: float, turn_ratio: float):
		try:
                        #  print(throttle,turn_ratio)
			self.lock.acquire()
			self.data = self.sensor_model(throttle, turn_ratio)
			self.lock.release()
		except KeyboardInterrupt:
			exit()
		return
	
	# @brief Returns the infromation inside the sensor.
	def sensor_model(self, throttle, turn_ratio):
		return [throttle, turn_ratio]
