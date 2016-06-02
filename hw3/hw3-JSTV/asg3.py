from flask import Flask, request, make_response, jsonify
from kazoo.client import KazooClient, KazooState
import requests, sys, os, logging, zc.zk

app = Flask(__name__)
app.debug = True
DT = {}

logging.basicConfig()



#Kazoo set up
def my_listener(state):
    if state == KazooState.LOST:
        print "lost connection"
    elif state == KazooState.SUSPENDED:
        print "suspended"
    else:
        print "reconnecting"

       


Emembers = os.getenv('MEMBERS')
Eport = (os.environ.get('PORT'))
Eip = (os.environ.get('IP'))
#zc = zc.zk.ZooKeeper(Eport+':'+Eport)
#zc.register('/cat/foo', ('0.0.0.0',8080))
print ("Members: "+ Emembers + " Port: " + Eport + " Ip: "+ Eip)
zk=KazooClient(hosts=Eport+':'+Eport)

zk.add_listener(my_listener)
zk.start()

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
    app.run(host="0.0.0.0",port=8080)