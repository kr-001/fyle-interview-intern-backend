# Dockerizing Fyle Interview Intern Backend

This guide will help you Dockerize your Fyle Interview Intern Backend Flask application, making it easy to build and run in a containerized environment.

## Prerequisites

- [Docker](https://www.docker.com/) installed on your machine.

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/kr-001/fyle-interview-intern-backend.git
    ```

2. Navigate to the project directory:

    ```bash
    cd fyle-interview-intern-backend
    ```

## Building the Docker Image

Build the Docker image using the provided Dockerfile:

```bash
docker build -t fyle-intern-backend:latest .
```

```bash
docker-compose up -d
```

Accessing the Flask Application
Visit http://localhost:7755 in your browser to access your Flask application.

Stopping the Docker Container
When you're done, stop and remove the Docker containers:

bash
Copy code
docker-compose down
Additional Information
Gunicorn Configuration: The application is run using Gunicorn with 4 workers. Adjust the configuration in the gunicorn_config.py file if needed.

Environment Variables: The FLASK_APP environment variable is set to core/server.py. Update it according to your project structure if necessary.

Database Migrations: If your application uses database migrations, they are applied during container startup. Ensure that your run.sh script or Dockerfile includes the necessary database setup.

Dockerfile: The Dockerfile contains instructions to set up the Python environment, copy project files, install dependencies, and define the entry point.

Docker Compose: The docker-compose.yml file orchestrates the Docker containers, exposing port 7755 on the host and mapping it to port 5000 in the container.
