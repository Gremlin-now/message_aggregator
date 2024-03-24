FROM python:3.11

WORKDIR /message_aggregator

COPY app.py .
COPY msgHandler.session .
COPY botHandlers.py .
COPY config.py .
COPY functions.py .
COPY userBotHandlers.py .
COPY .env .
COPY requirements.txt /
RUN pip install -r /requirements.txt

EXPOSE 443

CMD ["python", "app.py"]