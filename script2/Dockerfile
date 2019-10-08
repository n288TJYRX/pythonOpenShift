FROM python:3

COPY entrypoint2.py /
COPY DataInputStream.py /
COPY script2.py /

RUN pip install sh
RUN pip install pandas

EXPOSE 3306

ENTRYPOINT "python" "entrypoint2.py" "script2.py" "script2parameter" "JSON"
