FROM amazonlinux:latest
RUN yum -y update && yum -y install python3.11 python3-pip zip && yum clean all
RUN pip3 install virtualenv
WORKDIR /lambda-dependencies
RUN python3 -m venv python
# RUN source python/bin/activate
COPY requirements.txt .
# RUN pip3 install -r requirements.txt
# RUN zip -9 -r python.zip python
