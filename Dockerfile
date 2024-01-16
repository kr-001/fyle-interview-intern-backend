# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the core and tests directories into the container
COPY core /app/core
COPY tests /app/tests

# Copy other necessary files
COPY .gitignore /app
COPY Application.md /app
COPY Dockerfile /app
COPY gunicorn_config.py /app
COPY pytest.ini /app
COPY README.md /app
COPY requirements.txt /app
COPY run.sh /app
COPY core/server.py /app  

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variable
ENV FLASK_APP=core/server.py

# Run additional operations
CMD ["bash", "/app/run_container.sh"]
