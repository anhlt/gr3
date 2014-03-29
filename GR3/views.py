from django.shortcuts import render
from django.http import HttpResponse
from recommendation.model.classes import MatrixPreferenceDataModel as DataModel
from recommendation.metrics.pairwise import euclidean_distances
from recommendation.similarities.basic_similarities import ItemSimilarity
from recommendation.recommender.classes import ItemBasedRecommender
from recommendation.recommender.item_strategies import ItemsNeighborhoodStrategy
import datetime
import json
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Viewer')



critics={'anh': {'LadyRoom': 2.5, 'Cafe Moc': 3.5,
 'Cafe Blue': 3.0, 'CongVien': 3.5, 'Cafe Nhan': 2.5,
 'Rap Phim': 3.0},
'Hung': {'LadyRoom': 3.0, 'Cafe Moc': 3.5,
 'Cafe Blue': 1.5, 'CongVien': 5.0, 'Rap Phim': 3.0,
 'Cafe Nhan': 3.5},
'Quang': {'LadyRoom': 2.5, 'Cafe Moc': 3.0,
 'CongVien': 3.5, 'Rap Phim': 4.0},
'Long': {'Cafe Moc': 3.5, 'Cafe Blue': 3.0,
 'Rap Phim': 4.5, 'CongVien': 4.0,
 'Cafe Nhan': 2.5},
'Nha': {'LadyRoom': 3.0, 'Cafe Moc': 4.0,
 'Cafe Blue': 2.0, 'CongVien': 3.0, 'Rap Phim': 3.0,
 'Cafe Nhan': 2.0},
'Hai': {'LadyRoom': 3.0, 'Cafe Moc': 4.0,
 'Rap Phim': 3.0, 'CongVien': 5.0, 'Cafe Nhan': 3.5},
'Long': {'Cafe Moc':4.5,'Cafe Nhan':1.0,'CongVien':4.0}}

base_api_url = "http://harrenhal-php-97705.apse1.nitrousbox.com/elgg/services/api/rest/json/"

def current_datetime(request):
    payload = {'method': 'get.all.rating'}
    r = requests.get(base_api_url,params=payload)
    results = r.json()
    results = results['result']
    dataset = {}
    for result in results[:6000]:
	   if result['rating'] != 0:
            user_id = result['user_id']
            if user_id not in dataset:
                dataset[user_id] = {}
            dataset[user_id].update({result['page_id']:result['rating']})

    model =  DataModel(dataset)
    similarity = ItemSimilarity(model, euclidean_distances)
    items_strategy = ItemsNeighborhoodStrategy()
    recsys = ItemBasedRecommender(model, similarity, items_strategy)
    response_data = recsys.recommended(287)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


