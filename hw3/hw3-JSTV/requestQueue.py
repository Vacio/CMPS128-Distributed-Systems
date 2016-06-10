import requests, sys, os, Queue, datetime

class QueueNode(object):
	def __init__(self, item="", time=0.0, nextNode=None):
		self.node_item = item
		self.node_time = time
		self.nextNode = nextNode
	
	def set_item(self, item):
		self.node_item = item
	
	def set_time(self, time):
		self.node_time = time
	
	def get_item(self):
		return self.node_item
		
	def get_time(self):
		return self.node_time
		
	def set_next(self, node):
		self.nextNode = node
	
	def get_next(self):
		return self.nextNode
		
	def serialize(self):
		return {
			'item':self.node_item,
			'time':self.node_time
		}
		

class RequestQueue(object):
# json file, time
	# empty queue
	def __init__(self):
		self.head = None
		self.tail = None
		
	def push(self, item, time = datetime.time()):
		newNode = QueueNode(item, time)
		if (self.head == None):
			self.head = newNode
			self.tail = newNode
		else:
			newNode.set_next(self.tail)
			newNode = self.tail
			
	def pop(self):
		item = self.head.get_item()
		time = self.head.get_time()
		self.head = self.head.get_next()
		return (item,time)
	
	def serialize(self):
		return {
			'nodes':[self.head.serialize()]
		}
	
	def traverse(self)
		pointer = self.head
		while pointer is not None:
			pointer = pointer.get_next()
		return pointer