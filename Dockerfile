FROM centos:latest
RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y python34 python34-pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
# Assume that 'store' is the hostname of the datastore.
CMD [ "microcarddeck.py","http://store:5000/api/schema","--host","0.0.0.0" ]
