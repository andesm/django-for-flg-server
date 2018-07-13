FROM ubuntu:18.04
RUN apt-get -o Acquire::Check-Valid-Until=false updat && \
        apt-get -y install python3 python3-pip pandoc 
WORKDIR /django
COPY . /django
RUN pip3 install -r requirements.txt
COPY uwsgi.ini /django
ENTRYPOINT ["uwsgi", "uwsgi.ini"]
