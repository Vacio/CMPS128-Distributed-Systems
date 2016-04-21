from flask import Flask, request

app = Flask(__name__)
app.debug = True

@app.route("/kvs/<string:key_name>", methods=['GET', 'PUT', 'DELETE'])

def root(key_name):
	if (request.method == 'GET'):
		return "Get value of %s" % key_name

	if (request.method == 'PUT'):
		v = request.form['value']
		return "Stored %s at %s" % (v, key_name)

	if (request.method == 'DELETE'):
		return "Delete value and key: %s" % key_name
		
	else:
		return "Invalid request."

# Value GET (Key k) Get key-value pair using key
# PUT(Key k, Value v) Store key-value pair
# DEL(Key k) Remove key-value pair using key

# Responses for the GET, PUT, DEL methods

if __name__ == '__main__':
	app.run(port=8080)