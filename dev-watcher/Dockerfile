FROM python:3.11-slim

RUN apt-get update && apt-get install -y entr docker.io && rm -rf /var/lib/apt/lists/*

WORKDIR /watcher

COPY watcher.sh /watcher/watcher.sh

RUN chmod +x /watcher/watcher.sh

CMD ["/watcher/watcher.sh"]
