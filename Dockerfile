FROM python:alpine

LABEL maintainer="noe.berdoz@he-arc.ch"

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

RUN pip install --no-cache -r requirements.txt

CMD ["python", "app.py"]