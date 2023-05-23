FROM python:3.11.1-slim

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install scikit-learn


RUN pip install streamlit

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["stream_app.py"]
