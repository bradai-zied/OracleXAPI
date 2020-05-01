FROM python:3.7-alpine

RUN apk add --no-cache gcc libaio libc6-compat musl-dev python3-dev


WORKDIR /usr/app

COPY  app/*.py ./

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY instantclient_12_1.zip ./
RUN unzip instantclient_12_1.zip && \
    mv instantclient_12_1/ /usr/lib/ && \
    rm instantclient_12_1.zip && \
    ln /usr/lib/instantclient_12_1/libclntsh.so.12.1 /usr/lib/libclntsh.so && \
    ln /usr/lib/instantclient_12_1/libocci.so.12.1 /usr/lib/libocci.so && \
    ln /usr/lib/instantclient_12_1/libociei.so /usr/lib/libociei.so && \
    ln /usr/lib/instantclient_12_1/libnnz12.so /usr/lib/libnnz12.so && \
    ln /usr/lib/libnsl.so.2 /usr/lib/libnsl.so.1

ENV ORACLE_BASE /usr/lib/instantclient_12_1
ENV LD_LIBRARY_PATH /usr/lib/instantclient_12_1:/lib64
ENV TNS_ADMIN /usr/lib/instantclient_12_1
ENV ORACLE_HOME /usr/lib/instantclient_12_1
ENV DB_IP=default
ENV DB_PORT=default
ENV DB_SID=default
ENV DB_USER=default
ENV DB_PASSWORD=default

EXPOSE 5000
ENTRYPOINT [ "python", "./oracle_app.py"]