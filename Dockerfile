FROM python:3.8-alpine
WORKDIR /usr/app
COPY ./* ./

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_md

ENTRYPOINT uvicorn server:app