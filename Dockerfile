FROM python:3.5.2

RUN mkdir -p /home/sites/reporting
WORKDIR /home/sites/reporting

COPY ./requirements.txt /home/sites/reporting/requirements.txt
RUN pip3 install -r requirements.txt

CMD [ "python", "./main.py"]
