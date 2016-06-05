from flask import Flask, request, make_response, jsonify
import requests, sys, os
from linkedList import *
from requestQueue import * 

app = Flask(__name__)
app.debug = True

#personal node containing all it's own data
node_self = Node()
node_list = LinkedList()



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
    if mem!=name_me:
        node_list.insert(mem)

#print ("Node Name: "+ node_self.get_name()+ " status: " + str(node_self.get_status()) + " role: " + str(node_self.get_role()) + " port: " + node_self.get_port()+ " IP: " + node_self.get_IP())
node_list.print_node()

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
        


if __name__ == '__main__':    
    app.run(host=Eip,port=int(Eport))