FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]