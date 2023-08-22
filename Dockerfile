# Use an official Python runtime as the parent image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Set the `STREAMLIT_SERVER_PORT` environment variable
ENV STREAMLIT_SERVER_PORT=8502

# Make port 8502 available to the world outside this container
EXPOSE 8502

# Run streamlit app when the container launches
CMD ["streamlit", "run", "app.py"]
