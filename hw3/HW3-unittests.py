import unittest, requests, json

def test_a_put_nonexist():
    res = requests.put('http://192.168.99.100:49161'+'/kvs/foo', data={'val':'bart'})
    d=res.json()
    print ("TEST 1:")
    print (str(res.status_code) + ' = 201')
    print (str(d['replaced']) + ' = 0')
    print (d['msg'] + ' = success')
    print ("------------------")

def test_b_put_exist():
    res = requests.put('http://192.168.99.100:49163'+'/kvs/foo',data = {'val':'bart'})
    d=res.json()
    print ('TEST 2:')
    print (str(d['replaced']) + ' = 1')
    print (d['msg'] + ' = success')
    print ("------------------")

def test_c_get_nonexist():
    res = requests.get('http://192.168.99.100:49160'+'/kvs/faa')
    d = res.json()
    print ('TEST 3:')
    print (str(res.status_code) + ' = 404')
    print (d['error'] + ' = key does not exist')
    print (d['msg'] + ' = error')
    print ("------------------")

def test_d_get_exist():
    res = requests.get('http://192.168.99.100:49162'+'/kvs/foo')
    d = res.json()
    print ('TEST 4:')
    print (d['value'] + ' = bart')
    print (d['msg'] + ' = success')
    print ("------------------")

def test_e_del_nonexist():
    res = requests.delete('http://192.168.99.100:49164'+'/kvs/faa')
    d = res.json()
    print ('TEST 5:')
    print (str(res.status_code) + ' = 404')
    print (d['error'] + ' = key does not exist')
    print (d['msg'] + ' = error')
    print ("------------------")

def test_f_del_exist():
    res = requests.delete('http://192.168.99.100:49163'+'/kvs/foo')
    d = res.json()
    print ('TEST 6:')
    print (d['msg'] + ' = success')
    print ("------------------")

def test_g_get_deleted_key():
    res = requests.get('http://192.168.99.100:49161'+'/kvs/foo')
    d = res.json()
    print ('TEST 7:')
    print (str(res.status_code) + ' = 404')
    print (d['msg'] + ' = error')
    print (d['error'] + ' = key does not exist')
    print ("------------------")

def test_h_put_deleted_key():
    res = requests.put('http://192.168.99.100:49160'+'/kvs/foo',data= {'val':'bart'})
    d = res.json()
    print ("TEST 8:")
    print (str(res.status_code) + ' = 201')
    print (str(d['replaced']) + ' = 0')
    print (d['msg'] + ' = success')
    print ("------------------")

test_a_put_nonexist()
test_b_put_exist()
test_c_get_nonexist()
test_d_get_exist()
test_e_del_nonexist()
test_f_del_exist()
test_g_get_deleted_key()
test_h_put_deleted_key()