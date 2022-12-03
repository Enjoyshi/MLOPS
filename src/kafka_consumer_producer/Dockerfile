FROM python:3.9

WORKDIR /code

COPY src/kafka_consumer_producer/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY src/kafka_consumer_producer/partition.py /code/partition.py
COPY src/kafka_consumer_producer/save_consumer.py /code/save_consumer.py
COPY src/kafka_consumer_producer/predict_consumer1.py /code/predict_consumer1.py
# COPY src/kafka_consumer_producer/predict_consumer2.py /code/predict_consumer2.py
COPY src/kafka_consumer_producer/svm_model.joblib /code/svm_model.joblib

# CMD python partition.py && python save_consumer.py && python predict_consumer1.py && python predict_consumer2.py

CMD python predict_consumer1.py && python save_consumer.py

