FROM python:3.12-slim
ENV TZ=Asia/Seoul
RUN apt-get update && apt-get upgrade -y
WORKDIR /root/cloudflare-ddns
COPY app.py ./app.py
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3","app.py"]