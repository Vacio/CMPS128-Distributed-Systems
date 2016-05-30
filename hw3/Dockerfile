# Use a standard debian image
FROM debian:latest

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

# Change command to run python scripts
ENTRYPOINT ["python"]
CMD ["asg3.py"]