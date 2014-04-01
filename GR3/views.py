from django.shortcuts import render
from django.http import HttpResponse

import datetime
from recommendation.model.classes import MatrixPreferenceDataModel as DataModel
from recommendation.metrics.pairwise import euclidean_distances
from recommendation.similarities.basic_similarities import ItemSimilarity
from recommendation.recommender.classes import ItemBasedRecommender
from recommendation.recommender.item_strategies import ItemsNeighborhoodStrategy

import json
import requests
import logging
import django_rq
from django_rq import job

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Viewer')


base_api_url = "http://harrenhal-php-97705.apse1.nitrousbox.com/elgg/services/api/rest/json/"

def current_datetime(request):
    job = django_rq.enqueue(recommended,287)

    logger.debug(job.result())

    # return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse("Hello ")

@job
def recommended(user_id):
    payload = {'method': 'get.all.rating'}
    r = requests.get(base_api_url,params=payload)
    results = r.json()
    results = results['result']
    dataset = {}
    for result in results[:2000]:
       if result['rating'] != 0:
            user_id = result['user_id']
            if user_id not in dataset:
                dataset[user_id] = {}
            dataset[user_id].update({result['page_id']:result['rating']})
    model =  DataModel(dataset)
    similarity = ItemSimilarity(model, euclidean_distances)
    items_strategy = ItemsNeighborhoodStrategy()
    recsys = ItemBasedRecommender(model, similarity, items_strategy)
    response_data = recsys.recommended(user_id)
    logger.debug(response_data)
    return response_data
