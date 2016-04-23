from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
app.debug = True
DT = {}

@app.route("/kvs/<string:key_name>", methods=['GET', 'PUT', 'DELETE'])

def root(key_name):
	if (request.method == 'GET'):
		return "Get value of %s" % key_name

	if (request.method == 'PUT'):
		v = request.form['value']
		return putValue(key_name,v)

	if (request.method == 'DELETE'):
		return "Delete value and key: %s" % key_name

	else:
		return "Invalid request."

# Working
def putValue(key,value):
	if (key in DT):
		j = jsonify(msg='success',replaced=1)
		resp = make_response(j,200, {'Content-Type' : 'application/json'})
	else:
		j = jsonify(msg='success',replaced=0)
		resp = make_response(j,201,{'Content-Type' : 'application/json'})

	DT[key]=value
	return resp

if __name__ == '__main__':
	app.run(port=8080)