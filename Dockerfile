FROM python:3.6

# ME
MAINTAINER 4m3s0k0 g4j1 <nodirjon128.ng@gmail.com>

# Add code
COPY . /home/

# Set the working directory
WORKDIR /home/

RUN pip install -r requirements.txt

# Set environment variables
ENV FLASK_APP=main.py

# Expose the application's port
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
