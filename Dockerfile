FROM faucet/python3
WORKDIR /app
COPY rest_app.py /app
COPY db_connector.py /app
COPY PageNotFount.html /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 5000
VOLUME /app/logs
CMD python3 rest_app.py