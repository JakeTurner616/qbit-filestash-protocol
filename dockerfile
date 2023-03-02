FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y qbittorrent-nox

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install curl -y
RUN apt-get install dos2unix -y
# Copy the current directory contents into the container at /app
COPY config.txt /root/.config/qBittorrent/watched_folders.json
COPY config0.txt /root/.config/qBittorrent/qBittorrent.conf

COPY . /app


# Expose port 5001
EXPOSE 5001
EXPOSE 8080 

# Start the qBittorrent daemon and the Flask app
CMD qbittorrent-nox -d && python app.py 
COPY fileinput.sh /fileinput.sh
RUN mkdir -p downloads mnt tmp

