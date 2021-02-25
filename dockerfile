FROM python:3-buster

WORKDIR /opt/dockerhub

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/opt/dockerhub/check_docker_hub_limit.py" ]
