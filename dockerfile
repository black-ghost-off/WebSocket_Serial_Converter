FROM python:3.9

ADD . script/

WORKDIR script/

RUN pip install -r requirements.txt

CMD ["python", "main.py", "--port", "8800"]