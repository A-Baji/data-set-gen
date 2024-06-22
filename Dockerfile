FROM python:3.11
WORKDIR /main
RUN apt-get install git -y
COPY ./requirements.txt ./setup.py ./README.md /main/
COPY ./discordai_modelizer /main/discordai_modelizer
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir . && rm -R /main/*
