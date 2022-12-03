FROM python:3.9

WORKDIR /code

COPY src/save_consumer/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/save_consumer/save_consumer.py /code/save_consumer.py
COPY src/utils.py /code/utils.py

CMD python save_consumer.py