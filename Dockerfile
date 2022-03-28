FROM python:3.8-slim

COPY requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -i https://pypi.doubanio.com/simple -r /opt/app/requirements.txt

RUN  mkdir -p /flask_sample

COPY . /flask_sample
WORKDIR /flask_sample

EXPOSE 5000

CMD ["sh", "run.sh"]
