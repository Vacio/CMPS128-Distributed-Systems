# Use a standard debian image
FROM debian:latest

# Run updates and install pip,python,curl
RUN apt-get update && apt-get install -y \
	curl \
	python-pip \
	build-essential


# Copy the python app and set the directory.
COPY . /hw1docker
WORKDIR /hw1docker/hw1docker

# Install Flask
RUN pip install -r flaskcheck.txt

# Change command to run python scripts
ENTRYPOINT ["python"]
CMD ["server.py"]