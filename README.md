
# Sanitizer Microservice

Straightforward microservice that sanitizes/scrubs text provided to it via a REST API using the NLP technique of [named entity recognition](https://en.wikipedia.org/wiki/Named-entity_recognition)

Built with [spaCy](http://spacy.io) and [FastAPI](https://fastapi.tiangolo.com/)


## Usage 

Once run, the API will be at port 8000 by default

### Running locally

Install after cloning this repository. It is recommended that you use a virtual environment

```bash 
  pip install -r requirements.txt
  python -m spacy download en_core_web_md

```
Run it with

```
  uvicorn main:app --reload
```

### In Docker

Build and run:

```
  docker build -t sanitizer .
  docker run -d -it -p 8000:8080 sanitizer
```

## API Reference

#### Sanitize

```http
  POST /sanitize
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `text` | `string` | **Required**. The text that you want to sanitize 
| `sensitive_ents` | `string[]` | The entities you want sanitized out. They must be valid named entities, as specified by spaCy

Sanitizes text and returns the result
## Usage/Examples

```bash 
curl --location --request POST 'http://localhost:8000/sanitize' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "On 10-05-2020, John had met with with Marie"
}'
```
Response:

```json
{
    "sanitized_text": "On [REDACTED-DATE], [REDACTED-PERSON] had met with with [REDACTED-PERSON]"
}

```

  