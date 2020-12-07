FROM chinhrb/clc_server:v8
ENV PYTHONUNBUFFERED=1 POSTGRES_PASSWORD=${POSTGRES_PASSWORD} DB_IP=${DB_IP} ONMT_IP=${ONMT_IP} ELAS_IP=${ELAS_IP}
WORKDIR /clc_server
RUN git pull &&\
    pip3 install -r requirements.txt
    # python3 manage.py makemigrations &&\
    # python3 manage.py migrate






