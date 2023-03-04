FROM python:3.9-alpine

RUN apk add --no-cache qbittorrent-nox curl dos2unix wget unzip

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY config.txt /root/.config/qBittorrent/watched_folders.json
COPY config0.txt /root/.config/qBittorrent/qBittorrent.conf

COPY . /app/

RUN wget https://github.com/bill-ahmed/qbit-matUI/releases/download/v1.16.4/qbit-matUI_Unix_1.16.4.zip \
    && unzip qbit-matUI_Unix_1.16.4.zip -d /app \
    && rm qbit-matUI_Unix_1.16.4.zip

COPY fileinput.sh /fileinput.sh
RUN dos2unix /fileinput.sh

RUN mkdir -p downloads mnt tmp

EXPOSE 5001 

CMD qbittorrent-nox -d && python app.py
