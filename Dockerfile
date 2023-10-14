FROM python:3.9

RUN mkdir /library

WORKDIR /library

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /library/docker/*.sh