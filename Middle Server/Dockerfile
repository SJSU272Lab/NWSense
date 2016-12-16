#A simple Flask app container
FROM python:2.7
MAINTAINER Azhad "khoa.n.le@sjsu.edu"

#Place app in container
COPY . /app
WORKDIR /app

#Install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
