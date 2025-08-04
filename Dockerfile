FROM python:3.9-slim-buster

WORKDIR /myportfolio

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "app/__init__.py"]

EXPOSE 5000
