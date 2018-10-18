FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY ./book /book
COPY ./tests /tests
COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev
RUN pip install -r requirements.txt
ENV PYTHONPATH=/book
ENV FLASK_APP=book
ENV FLASK_ENV=development
EXPOSE 5000
RUN flask init-db
CMD ["flask", "run", "--host=0.0.0.0"]