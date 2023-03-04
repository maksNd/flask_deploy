FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /code
COPY run.py .

CMD flask --app=run.py run -h 0.0.0.0 -p 8080
#CMD gunicorn run:app -b 0.0.0.0:80