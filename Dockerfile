FROM python:latest
ADD . /usr/bin
WORKDIR /usr/bin
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "amcli.py"]
CMD ["-h"]
