import os
from datetime import datetime
from typing import Optional

from elasticsearch import Elasticsearch
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

ELASTICSEARCH_URL = os.environ["ELASTICSEARCH_URL"]
ELASTICSEARCH_PORT = os.environ["ELASTICSEARCH_PORT"]
ELASTICSEARCH_INDEX = os.environ["ELASTICSEARCH_INDEX"]

elasticsearch = Elasticsearch("{}:{}".format(ELASTICSEARCH_URL, ELASTICSEARCH_PORT))


@app.get("/search/")
async def search(
    name: Optional[str] = Query(None, description="Filter by name (text field)"),
    username: Optional[str] = Query(
        None, description="Filter by username (keyword field)"
    ),
    category: Optional[str] = Query(
        None, description="Filter by category (keyword field)"
    ),
    text: Optional[str] = Query(None, description="Filter by text (text field)"),
    inserted_at: Optional[str] = Query(
        None, description="Filter by inserted_at (date field) in 'YYYY-MM-DD' format"
    ),
):
    query = {"query": {"bool": {"must": []}}}

    if name:
        query["query"]["bool"]["must"].append({"match": {"name": name}})
    if username:
        query["query"]["bool"]["must"].append({"term": {"username": username}})
    if category:
        query["query"]["bool"]["must"].append({"term": {"category": category}})
    if text:
        query["query"]["bool"]["must"].append({"match": {"text": text}})
    if inserted_at:
        try:
            inserted_at_date = datetime.strptime(inserted_at, "%Y-%m-%d").date()
            query["query"]["bool"]["must"].append(
                {"range": {"inserted_at": {"gte": inserted_at_date}}}
            )
        except ValueError:
            return {"error": "inserted_at must be in 'YYYY-MM-DD' format"}

    response = elasticsearch.search(index=ELASTICSEARCH_INDEX, body=query)

    return JSONResponse(
        {
            "hits": response["hits"]["hits"],
            "total": response["hits"]["total"]["value"],
        },
        status_code=200,
    )


@app.get("/health/")
async def health_check():
    return JSONResponse(
        content={"status": "healthy"},
        status_code=200,
    )
