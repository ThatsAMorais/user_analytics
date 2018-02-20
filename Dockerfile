FROM python:3

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP "narrative_user_analytics.py"
RUN mkdir -p /opt/services/flaskapp/src
#VOLUME ["/opt/services/flaskapp/src"]
COPY requirements.txt /opt/services/flaskapp/src/
WORKDIR /opt/services/flaskapp/src
RUN pip install -r requirements.txt
COPY . /opt/services/flaskapp/src
EXPOSE 5000
CMD ["python", "narrative_user_analytics.py"]
