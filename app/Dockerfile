FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY src /app/src
COPY main.py main.py
COPY wait-services.sh wait-services.sh
RUN chmod +x wait-services.sh

# для запуска на винде
RUN sed -i 's/\r//' wait-services.sh

CMD ["./wait-services.sh", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
