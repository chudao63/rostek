import time, logging, schedule, threading

class Scheduling(threading.Thread):
	"""Loading các công việc cần làm

	Args:
		actions = {
			1 : {
				"time" : "13:29",
				"func" : printer
			}
		}
	"""
	def __init__(self, threadId = 1):
		threading.Thread.__init__(self)
		self.counter = 1
		self.active = True
		self.threadId = threadId
		
	def loading(self):
		"""Loading schedule time
		"""
		try:
			schedule.clear()
			for actionId in Actions.get_instance().actions:
				action = Actions.get_instance().actions[actionId]
				print("Add schedule at ", action["time"] )
				schedule.every().day.at(action["time"]).do(action["func"])
				# schedule.every(5).seconds.do(action["func"])
		except Exception as e:
			logging.error(str(e))
		
	def run(self):
		""" RUNNING THREAD
		"""
		global threadId
		# print ("Starting")
		self.loading()
		while True:
			schedule.run_pending()
			time.sleep(1)
			# print(self.threadId)
			if not self.active:
				break
		# print ("Exiting")

	def release(self):
		""" RELEASE THREAD
		"""
		self.active = False

class Actions:
	__instance = None
	@staticmethod
	def get_instance():
		if Actions.__instance == None:
			Actions()
		return Actions.__instance
	
	def __init__(self):
		self.actions = {}
		self.threadId = 1
		self.scheduleThread = None
		if Actions.__instance != None:
			raise Exception("Do not call __init__().")
		else:
			Actions.__instance = self

	def get_action(self):
		""" Return all action in scheduling
		"""
		print("get actual schedule:", schedule.get_jobs())
		actions = {

		}
		for action in self.actions:
			actions[action] = self.actions[action]["time"]
		return {
			"actions" : actions
		}

	def add_action(self, action):
		""" Add new action
		"""
		self.actions.update(action)
		if self.scheduleThread:
			self.scheduleThread.release()
		self.scheduleThread = Scheduling(self.threadId)
		self.scheduleThread.start()
		self.threadId += 1
	
	def remove_action(self, actionId):
		""" Remove action with action id
		"""
		if actionId in self.actions:
			self.actions.pop(actionId)
			if self.scheduleThread:
				self.scheduleThread.release()
			time.sleep(1)
			self.scheduleThread = Scheduling(self.threadId)
			self.scheduleThread.start()
			self.threadId += 1

	def clear_all_action(self):
		""" Clean all action
		"""
		self.actions = {}
		if self.scheduleThread:
			self.scheduleThread.release()
		schedule.clear()