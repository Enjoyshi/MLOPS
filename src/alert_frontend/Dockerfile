FROM python:3.9

WORKDIR /code

COPY src/alert_frontend/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/utils.py /code/utils.py
COPY src/alert_frontend/frontend.py /code/frontend.py

CMD streamlit run frontend.py --server.port 8502