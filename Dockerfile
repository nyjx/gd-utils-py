FROM python:alpine

WORKDIR /
RUN apk add git
RUN git clone https://github.com/nyjx/gd-utils-py

WORKDIR gd-utils-py

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /gd-utils-py/files

CMD ["sh","/gd-utils-py/start.sh"]