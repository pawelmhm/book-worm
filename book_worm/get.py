import json
import re

from elasticsearch import Elasticsearch
es = Elasticsearch()

terms = 'polski faszyzm'
publication_name = 'mysl_narodowa'
match_query_type = 'match_phrase' # 'match'

query = {
  "query": {
    "bool": {
      "must": {
        match_query_type: {
          "text": terms
        }
      },
      "filter": {
        "term": {
          "publication_name": publication_name
        }
      }
    }
  }
}

res = es.search(index='scrapy-2018-06', body=query)

total = res['hits']['total']
if not total:
  print("no results")
prett = []
for hit in res['hits']['hits']:
    source = hit['_source']
    text = source.pop('text', '')
    pieces = []
    for match in re.finditer(terms, text, re.I):
        piece = text[match.start(0)-200: match.end(0) + 200]
        pieces.append(piece)

    source['piece'] = pieces
    prett.append(source)

print(json.dumps(prett))