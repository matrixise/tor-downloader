#
# Dockerfile for youtube-worker
#

FROM python:3.8-alpine
MAINTAINER kev <noreplay@easypi.pro>

RUN apk add -U ca-certificates neovim ffmpeg \
    && rm -rf /var/cache/apk/* \
    && pip install redis youtube-dl pdbpp

COPY worker.py /code/
VOLUME /data
WORKDIR /data

#CMD ["sleep", "infinity"] # ["python", "/code/worker.py"]
CMD ["python", "/code/worker.py"]
