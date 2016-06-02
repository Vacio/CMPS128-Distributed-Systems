# Use a standard debian image
FROM java:7

# Run updates and install pip,python,curl
RUN apt-get update && apt-get install -y \
	curl \
	python-pip \
	build-essential


# Copy the python app and set the directory.
COPY . /hw3-JSTV
WORKDIR /hw3-JSTV/hw3-JSTV

# Install Flask
RUN pip install Flask

#install kazoo
RUN pip install kazoo

#install zookeeper
CMD /zookeeper-3.4.8/bin/zkServer.sh start

# Change command to run python scripts
ENTRYPOINT ["python"]
CMD ["asg3.py"]