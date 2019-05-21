FROM python

ARG PORT=3000
ENV PORT $PORT

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app_api.py"]
