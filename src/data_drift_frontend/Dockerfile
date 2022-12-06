FROM python:3.9

WORKDIR /code

COPY src/data_drift_frontend/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/data_drift_frontend/frontend.py /code/frontend.py

CMD streamlit run frontend.py --server.port 8501