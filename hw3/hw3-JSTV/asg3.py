from flask import Flask, request, make_response, jsonify
from linkedList import *
from requestQueue import * 
import requests, sys, os, json, threading, time


app = Flask(__name__)
app.debug = True
DT = {}
#personal node containing all it's own data
node_self = Node()
node_list = LinkedList()

#global variables
Emembers = os.getenv('MEMBERS')
Eport = (os.environ.get('PORT'))
Eip = (os.environ.get('IP'))
members = Emembers.split(',')
name_me = str(Eip+':'+Eport)


node_self.set_name(name_me)
node_self.set_status(1) 
node_self.set_role(0)
node_self.set_IP(Eip)
node_self.set_port(Eport)
for mem in members:
	node_list.insert(mem)
node_list.update_node(name_me,1, 0, None,None)
node_list.update_node(name_me,1, 0, None,None)

	
#print ("Node Name: "+ node_self.get_name()+ " status: " + str(node_self.get_status()) + " role: " + str(node_self.get_role()) + " port: " + node_self.get_port()+ " IP: " + node_self.get_IP())
#print(node_list.print_node())
'''node_list.update_node('10.0.0.21:12346',1, 0, None,None)
print(node_list.print_node())'''
# def pingNode(destName, node_self):
# 	r = requests.get('http://'+destName+'/ack')
# 	return r.text
	

def pingNode(destName):
	try:
		r = requests.get('http://'+destName+'/ack', timeout=2)
		#update node's data if found 
		if (r.status_code == 200):
			ping = json.loads(r.text)
			pName = ping['name']
			pStatus = ping['status']
			pRole = ping['role']
			pLeader = ping['leader']
			pQueue = ping['queue']
			pingStatus = node_list.update_node(pName,pStatus, pRole, pLeader,pQueue)
			if pingStatus == -1:
				cat += destName +"ERROR\n"
				return cat
			cat = destName + " Success\n"
			return cat
	except (requests.ConnectionError, requests.HTTPError, requests.Timeout):	
		#set the node status to dead if response not given
		n = node_list.search_node(destName)
		n.set_status(0)
		cat = destName +" Dead \n"
		return cat

# Recieves node and Prints the node object.
@app.route('/ack', methods=['GET'])
def ack():
	payload = jsonify(name=node_self.get_name(), ip=node_self.get_IP(), port=node_self.get_port(), status=node_self.get_status(), role=node_self.get_role(), leader=node_self.get_leader(), queue='Queue')
	return make_response(payload,200,{'Content-Type':'application/json'}) #{'http://'+destName+'/ack', data=payload)

@app.route("/kvs/<string:key_name>", methods=['GET', 'PUT', 'DELETE'])
def root(key_name):
	if (request.method == 'GET'):
		return getValue(key_name)

	if (request.method == 'PUT'):
		v = request.form['val']
		return putValue(key_name,v)

	if (request.method == 'DELETE'):
		#return "Delete value and key: %s" % key_name
		return delValue(key_name)
	else:
		return "Invalid request."
# Working
def getValue(key):
	if (key in DT):
		value = DT[key]
		j = jsonify(msg='success',value=value)
		return make_response(j,200,{'Content-Type':'application/json'})
	else:
		j = jsonify(msg='error',error='key does not exist')
		return make_response(j,404,{'Content-Type':'application/json'})
# Working
def putValue(key,value):
	if (key in DT):
		DT[key]=value
		j = jsonify(msg='success',replaced=1)
		return make_response(j,200, {'Content-Type' : 'application/json'})
	else:
		DT[key]=value
		j = jsonify(msg='success',replaced=0)
		return make_response(j,201,{'Content-Type' : 'application/json'})
# idk
def delValue(key):
	if (key in DT):
		DT.pop(key,None)
		j = jsonify(msg='success')
		return make_response(j,200,{'Content-Type':'application/json'})
	else:
		j = jsonify(msg='error',error='key does not exist')
		return make_response(j,404,{'Content-Type':'application/json'})
        
# Tests pinging to node 10.0.0.21:12346
@app.route("/testping", methods=['GET'])
def getPing(mem):
	# 'http://10.0.0.21:12346/kvs/foo'
	# r = requests.get('http://'+members[1]+'/kvs/foo', timeout = 3)
	cat = ""
	cat += pingNode(mem)
	cat += node_list.print_node()
	print cat

def heartbeat():
	while True:
		for mem in members:
			if (name_me!=mem):
				#threading.Timer(5.0, getPing, (mem,)).run()
				getPing(mem)
		sys.stdout.flush()		
		time.sleep(4.0)

if __name__ == '__main__':
	#heartbeat()
	threading.Timer(2.0,heartbeat).start()
	app.run(host=Eip,port=int(Eport))