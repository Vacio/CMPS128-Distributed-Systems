#Linked List python file for each node specification

#Status (at least, what you think it is):
# 0 = dead
# 1 = alive


#Role: 1 = leader
#      0 = backup

# from requestQueue import *
from flask import jsonify
import time
class Node(object):
    def __init__(self,Name=None,IP=None, Port=None, Status=0, Role=0, Leader="", Queue={}, nextNode=None, LeaderElection=False):
        self.Name = Name
        self.IP = IP
        self.Port=Port
        self.Status=Status
        self.Role = Role
        self.Leader=Leader #set leader variable to port
        self.Queue=Queue
        self.nextNode=nextNode
        self.LeaderElection=LeaderElection
    
    def get_port(self):
        return self.Port
    
    def set_port(self, port):
        self.Port= port
    
    def get_IP(self):
        return self.IP
    
    def set_IP(self, ip):
        self.IP = ip
    
    def get_name(self):
        return self.Name
    
    def set_name(self, name):
        self.Name= name
    
    def set_status(self, status):
        self.Status = status
        
    def get_status(self):
        return self.Status
    
    def set_role(self,role):
        self.Role = role
    
    def get_role(self):
        return self.Role
    
    def set_leader(self,leader):
        self.Leader = leader
    
    def get_leader(self):
        return self.Leader
    
    def set_queue(self, queue):
        self.Queue = queue

    def addQueue(self,method, key, value):
        tick = time.time()
        self.Queue[tick] = (method, key, value)
        return self.Queue[tick]
        
    def printQueue(self):
        cat =str(self.get_name())+" Queue: "
        for keys,values in self.Queue.items():
            cat += str(keys)
            cat +=" !!!!! "
            method,key,value = values
            cat += method+" " + key + " " +value+"\n"
        #for i in self.Queue:
        #    cat += str(i) +" "
        #    for n in self.Queue[i]:
        #        cat += str(n)+":"+ self.Queue[i][n]
        return cat
    
    def subQueue(self, queue):
       return queue.pop(min(queue.keys(),key=int))
       
    def mergeQueue(self, queue):
        for ticks in queue:
            if(self.Queue[tick] !=  queue[tick]):
                method,key,value=queue.items()
                self.addQueue(method,key,value)
        
    def get_queue(self):
        return self.Queue
    
    def set_next(self, next):
        self.nextNode = next
    
    def get_next(self):
        return self.nextNode
        
    def set_LE(self, LE):
        self.LeaderElection = LE
    
    def get_LE(self):
        return self.LeaderElection
        
class LinkedList(object):

    def __init__(self,head=None):
        self.head = head
        
    def insert(self,Name,IP,Port):
        n = Node(Name,IP,Port)
        n.set_next(self.head)
        self.head = n
    
    def search_node(self,Name):
        pointer = self.head
        found = False
        while pointer and found is False:
            if (pointer.get_name() == Name):
                found = True
                return pointer
            else:
                pointer = pointer.get_next()
        return pointer
		
    def update_node(self, Name, status, role, leader, queue, LE):
        n = self.search_node(Name)
        if n is None:
            return -1
        n.set_status(status)
        n.set_role(role)
        n.set_leader(leader)
        n.set_queue(queue)
        n.set_LE(LE)
        return 1
        
    def node_status(self,Name):
        n = self.search_node(Name)
        if n is None:
            return ""
        return n.get_status()
        
    def node_role(self,Name):
        n = self.search_node(Name)
        if n is None:
            return ""
        return n.get_role()
        
    def node_queue(self,Name):
        n = self.search_node(Name)
        if n is None:
            return ""
        return n.get_queue()
        
    def node_leader(self,Name):
        n = self.search_node(Name)
        if n is None:
            return ""
        return n.get_leader()
        
    def isThereALeader(self, Snode):
        pointer = self.head
        overallLeader = 0
        overallNameofLeader = "LEADER"
        while pointer is not None:
            if (pointer.get_status==1):
               node_L = pointer.get_leader()
               overallNameofLeader = node_L
               #if node_L != "":
                    #ip,port=node_L.split(":")
                    #if overallLeader<int(port):
                    #overallLeader=port
                    #overallNameofLeader = ip+":"+port
        #cip,currentLeader = Snode.get_leader().split(":")
        #if overallLeader > int(currentLeader):
            #print ("sarah did good -"+overallNameofLeader +"\n")
            #Snode.set_leader(overallNameofLeader)
        #   return overallNameofLeader
        return overallNameofLeader
    
    def print_node(self):
        pointer = self.head
        cat = ""
        while pointer is not None:
            cat += ("Name: "+ pointer.Name + " Status: "+ str(pointer.Status) +" Role: " +str(pointer.Role) + " Leader: "+ pointer.Leader+" LE: "+ str(pointer.LeaderElection)+"\n")
            pointer = pointer.nextNode
        return cat