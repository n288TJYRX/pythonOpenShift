FROM python:3

COPY entrypoint1.py /
COPY DataInputStream.py /
COPY script1.py /

RUN pip install sh
RUN pip install pandas

EXPOSE 3306

ENTRYPOINT "python" "entrypoint1.py" "script1.py" "script1parameter" "JSON"
