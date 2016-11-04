# Use lightweight linux distro
FROM alpine:3.1

# install pip
RUN apk add --update python py-pip

# install requirements
ADD requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt

# run app
ADD . /opt/app
CMD ["python", "/opt/app/notifier.py"]
