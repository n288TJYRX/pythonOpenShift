FROM python:3

COPY entrypoint.py /
COPY DataInputStream.py /

RUN pip install sh

EXPOSE 3306

ENTRYPOINT "python" "entrypoint.py"
