# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /codeForDeploy

# Copy the requirements file to the working directory
COPY requirements.txt /codeForDeploy/

# Install project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code to the working directory
