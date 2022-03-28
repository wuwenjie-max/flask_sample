FROM python:3.8-slim

COPY requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -i https://pypi.doubanio.com/simple -r /opt/app/requirements.txt

RUN  mkdir -p /project

COPY . /project
WORKDIR /project

EXPOSE 5000

CMD ["sh", "run.sh"]
