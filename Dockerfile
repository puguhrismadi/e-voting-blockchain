# Base image
FROM python:3.9-slim-buster

# Set working directory
RUN mkdir /code
COPY . /code
COPY requirements.txt /code
COPY app.py /code
COPY service.py /code
WORKDIR /code

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 3333
EXPOSE 4444

# Set entrypoint command
CMD ["sh", "-c", "python app.py & python service.py"]
