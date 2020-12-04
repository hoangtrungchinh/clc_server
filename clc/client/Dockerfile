FROM chinhrb/clc_client:v1
ENV PYTHONUNBUFFERED=1 SERVER_URL=${SERVER_URL}
WORKDIR /clc_client
RUN git pull && pip3 install -r requirements.txt && python3 manage.py migrate