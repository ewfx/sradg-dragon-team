FROM python:3.10-slim

ENV API_KEY ="f6345bc740864de492e19f428faf0fa0"
ENV CUDA_VISIBLE_DEVICES="-1"

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


COPY . /app

ENTRYPOINT ["python3"]

CMD ["main.py"]
