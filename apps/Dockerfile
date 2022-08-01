FROM python:3.8

WORKDIR /app

COPY ./apps/requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

## 도커라이즈 설치
#ENV DOCKERIZE_VERSION v0.6.1
#RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
#    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
#    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
#
## DB연결되기까지 15초 대기시간을 설정
#ENTRYPOINT ["dockerize", "-wait", "15s"]