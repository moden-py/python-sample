FROM python:3.5
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT python run.py
