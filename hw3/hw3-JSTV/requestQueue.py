class QueueNode(object):
	def __init__(self, item, time):
		jsonFile = item
		timeStamp = time

class RequestQueue(object):
# json file, time
	# empty queue
	def __init__(self):
		self.head = none
		self.tail = node
		
	def push(self, item, time = datetime.time()):
		newNode = QueueNode(item, time)
		if (self.head == None):
			self.head = newNode
			self.tail = newNode
		else:
			self.tail = newNode
	def pop(self):
		item = self.head.jsonFile
		time = self.head.timeStamp
		self.head = self.tail
		return (item,time)