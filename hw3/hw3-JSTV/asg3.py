from flask import Flask, request, make_response, render_template, jsonify, redirect
from linkedList import *
# from requestQueue import * 
import requests, sys, os, json, threading, time
from logging.handlers import RotatingFileHandler


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
startElection=False

##TESTING##
#print ("Node Name: "+ node_self.get_name()+ " status: " + str(node_self.get_status()) + " role: " + str(node_self.get_role()) + " port: " + node_self.get_port()+ " IP: " + node_self.get_IP())
#print(node_list.print_node())
# node_list.update_node('10.0.0.21:12346',1, 0, None,None)
# print(node_list.print_node())'''
# def pingNode(destName, node_self):
#     r = requests.get('http://'+destName+'/ack')
#     return r.text

def initThisNode():
    node_self.set_name(name_me)
    node_self.set_IP(Eip)
    node_self.set_port(Eport)
    node_self.set_status(1) 
    node_self.set_role(1)
    node_self.set_queue({})
    node_self.set_leader(name_me)
    node_self.set_LE(False)
    for mem in members:
        if mem != name_me:
            mIP,mPort=mem.split(":")
            node_list.insert(mem,mIP,mPort)
    #node_list.update_node(name_me,1, 0, name_me,"")
    
def checkLeader(pLeader):
    currLeader = node_self.get_leader()
    cIP,cPort=currLeader.split(":")
    nIP,nPort=pLeader.split(":")
    if nPort > cPort:
        node_self.set_leader(pLeader)
        if pLeader != name_me:
            node_self.set_role(0)
            #insert transfer here
        else:
            node_self.set_role(1)

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
            pPort = ping['port']
            pQueue = ping['queue']
            pLE = ping['LE']
          #  if pLE == False:
          #      startElection = False
            checkLeader(pLeader)
            pingStatus = node_list.update_node(pName,pStatus, pRole, pLeader,pQueue, pLE)
            if pingStatus == -1:
                cat += destName +"ERROR\n"
                return cat
            cat = destName + " Success\n"
            return cat
    except(requests.ConnectionError, requests.HTTPError, requests.Timeout):    
        #set the node status to dead if response not given
        n = node_list.search_node(destName)
        n.set_status(0)
        n.set_leader(":")
        n.set_role(0)
        if (node_self.get_leader()==destName):
            node_self.set_leader(" : ")
            node_self.set_LE(True)
            #n.set_LE(True)
            leaderElection()
        cat = destName +" Dead \n"
        return cat

# Recieves node and Prints the node object.
@app.route('/ack', methods=['GET'])
def ack():
    payload = jsonify(name=node_self.get_name(), ip=node_self.get_IP(), port=node_self.get_port(), status=node_self.get_status(), role=node_self.get_role(), leader=node_self.get_leader(), queue=node_self.get_queue(), LE=node_self.get_LE())
    return make_response(payload,200,{'Content-Type':'application/json'}) #{'http://'+destName+'/ack', data=payload)

@app.route("/kvs/<string:key_name>", methods=['GET', 'PUT', 'DELETE'])
def root(key_name):
    # All Should do
    if (request.method == 'GET'):
        return getValue(key_name)
    # If i am a Leader
    if (node_self.get_role()==1):
        v = request.form['val']
        if (request.method == 'PUT'):
            node_self.addQueue('PUT',key_name,v)
            return putValue(key_name, v)

        if (request.method == 'DELETE'):
            node_self.addQueue('DELETE',key_name,"")
            return delValue(key_name)

        else:
            return "Leader, Invalid Request"
    # If I am a Backup
    if (node_self.get_role()==0):
        # if Request was from Leader, Do the command
        if (request.remote_addr == (node_self.get_leader())[:-6]):
            v = request.form['val']
            if (request.method == 'PUT'):
                return putValue(key_name,v)
            if (request.method == 'DELETE'):
                return delValue(key_name)
        # if Request was NOT from a leader, send the request to my leader     
        else:
            v = request.form['val']
            if (request.method == 'PUT'):
                url = 'http://'+node_self.get_leader()+'/kvs/'+key_name
                res = requests.put(url,data={'val' : v})
                return 'Sent PUT Request to Leader'
            if (request.method == 'DELETE'):
                url = 'http://'+node_self.get_leader()+'/kvs/'+key_name
                res = requests.delete(url)
                return 'Sent DEL Request to Leader'
            else:
                return 'Not Leader, Invalid Request'
    else:
            return "Invalid request."
    
    
def leaderDuties():
    lQueue = node_self.get_queue()
    # return node_self.subQueue(node_self.get_queue())
    cat = "LEADER DUTY: "  
    cat += str(bool(lQueue)) +" "+ node_self.printQueue()
    if bool(lQueue):
        task = node_self.subQueue(lQueue)
        method, keyname, value = task
        #return "Made to broadcast!"
        leaderBroadcast(method,keyname,value)
        return cat + " Good"
    return cat + " BAAAAAD"
         
def leaderBroadcast(method, keyname, value):
    for mem in members:
        if mem != name_me:
            pointer = node_list.search_node(mem)
            if (pointer.get_status()==1):
                leaderMessage(method,keyname,value,pointer.get_name())
              
                    
        
def leaderMessage(method,keyname,value,nodeName):
    url = 'http://'+nodeName+'/kvs/'+keyname
    try:
        if (method=='PUT'):
            res = requests.put(url, timeout=2, data={'val' : value})
        else:
            res = requests.delete(url, timeout=2)
    except (requests.ConnectionError, requests.HTTPError, requests.Timeout):
        getPing(nodeName)
        pointer = node_list.search_node(nodeName)
        if (pointer.get_status()==1):
            leaderMessage(method,keyname,value)
    


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
    cat += str(pingNode(mem))
    cat += node_list.print_node()
    print cat
    
def leaderElection():
    newLeader=0
    newLeaderName =":"
    for mem in members:
        if (name_me!=mem):
            pointer = node_list.search_node(mem)
            if (pointer.get_status()==1):
                if int(pointer.get_port()) > newLeader:
                    newLeader= pointer.get_port()
                    newLeaderName=pointer.get_name()
    if int(node_self.get_port()) > newLeader:
        newLeader= node_self.get_port()
        newLeaderName=node_self.get_name()
    node_self.set_leader(newLeaderName)
    node_self.set_LE(False)
    
def heartbeat():
    startElection=False
    while True:
        for mem in members:
            if (name_me!=mem):
                #threading.Timer(5.0, getPing, (mem,)).run()
                getPing(mem)
        sys.stdout.flush()   
        if(int(node_self.get_role()) == 1):
            print leaderDuties()

        time.sleep(6.0)

if __name__ == '__main__':
    #heartbeat()
    initThisNode()
    threading.Timer(2.0,heartbeat).start()
    app.run(host=Eip,port=int(Eport))