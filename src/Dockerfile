FROM python:3.9.7-buster
EXPOSE 8000
WORKDIR /src
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
ENV PYTHONPATH /