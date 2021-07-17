# this is an official Python runtime, used as the parent image
FROM python:3.6.5-slim

# set the working directory in the container to /app
WORKDIR /front_end

# add the current directory to the container as /app
COPY . /front_end

# execute everyone's favorite pip command, pip install -r
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# unblock port 35303 for the Flask app to run on
EXPOSE 35303

# execute the Flask app
CMD ["python", "frontend_server1.py"]