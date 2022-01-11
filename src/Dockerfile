FROM python:3.9.7-buster
EXPOSE 8000
WORKDIR /src
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
ENV PYTHONPATH /
CMD ["gunicorn", "wsgi_app:app", "-b", "0.0.0.0:8000", "-w", "2", "--log-level", "debug", "--timeout", "0" ]