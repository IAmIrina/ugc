FROM python:3.10-buster

RUN  groupadd -r runner --gid=1280 && useradd -r -g runner --uid=1280 --create-home --shell /bin/bash runner

COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


COPY ./src /home/runner/
USER runner
WORKDIR /home/runner

CMD python3 benchmark.py
