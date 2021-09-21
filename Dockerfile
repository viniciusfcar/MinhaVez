FROM python:3

ENV PYTHONUNBUFFERED 1

# create the appropriate directories
ENV HOME=/home/app

RUN mkdir -p $HOME
RUN mkdir $HOME/staticfiles
RUN mkdir $HOME/media
WORKDIR /home/app
COPY requirements.txt /home/app/
RUN pip install -r requirements.txt
COPY . /home/app/