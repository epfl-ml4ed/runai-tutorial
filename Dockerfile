# Use the minimalistic Python Alpine image for smaller size.
FROM python:3.9-alpine

# Set the working directory in docker
WORKDIR /app

# Create a directory for the data volume
RUN mkdir /results

# Copy the Python script into the container at /app
COPY write_text.py .

# Always use the Python script as the entry point
ENTRYPOINT ["python", "write_text.py"]

# By default, write "hello world" to the file.
CMD ["--text", "hello world"]
