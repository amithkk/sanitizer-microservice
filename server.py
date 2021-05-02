from typing import Optional

import spacy
from fastapi import FastAPI, HTTPException

# Change to TRF model for more accuracy
from pydantic import BaseModel

nlp = spacy.load('en_core_web_md')
app = FastAPI()


class Sanitizable(BaseModel):
    text: str
    sensitive_ents: Optional[str] = ['PERSON', 'DATE']


def anonymize(token, sensitive_ents):
    if token.ent_type_ in sensitive_ents:
        has_space = len(token.text_with_ws) != len(token.text)
        return "[REDACTED-%s]%s" % (token.ent_type_, " " if has_space else "")
    else:
        return token.text_with_ws


def spacy_sanitize(text, sensitive_ents):
    sp_doc = nlp(text)
    with sp_doc.retokenize() as retokenizer:
        for ent in sp_doc.ents:
            retokenizer.merge(ent)
    tokens = map(lambda doc_iterable: anonymize(doc_iterable, sensitive_ents), sp_doc)
    return "".join(tokens)


@app.post("/sanitize")
def sanitize(sanitizable_item: Sanitizable):
    try:
        sanitized_text = spacy_sanitize(sanitizable_item.text, sanitizable_item.sensitive_ents)
        return {"sanitized_text": sanitized_text}
    except Exception:
        raise HTTPException(status_code=500, detail="Sanitization Failure. ")
