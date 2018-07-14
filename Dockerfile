FROM ubuntu
ENV LANG C.UTF-8
RUN  apt-get update && apt-get -y install python3 python3-pip pandoc 
WORKDIR /django
COPY . /django
RUN pip3 install -r requirements.txt
COPY uwsgi.ini /django
ENTRYPOINT ["uwsgi", "uwsgi.ini"]
