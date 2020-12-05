FROM chinhrb/clc_server:v6
ENV PYTHONUNBUFFERED=1
WORKDIR /clc_server
RUN git pull &&\
    pip3 install -r requirements.txt &&\
    python3 manage.py makemigrations &&\
    python3 manage.py migrate