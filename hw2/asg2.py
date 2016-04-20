from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route("/kvs/<string:key_name>", methods=['GET', 'PUT'])

def root():
	if (request.method == 'GET'):
def show_keyname(key_name):
	return "Key: %s" % key_name

# Value GET (Key k) Get key-value pair using key
# PUT(Key k, Value v) Store key-value pair
# DEL(Key k) Remove key-value pair using key

# Responses for the GET, PUT, DEL methods

if __name__ == '__main__':
	app.run(port=8080)