import json
import logging

from django.http import HttpResponse
import requests
import django_rq
from django_rq import job
from rq.job import Job

from recommendation.model.classes import MatrixPreferenceDataModel as DataModel
from recommendation.metrics.pairwise import euclidean_distances
from recommendation.similarities.basic_similarities import ItemSimilarity
from recommendation.recommender.classes import ItemBasedRecommender
from recommendation.recommender.item_strategies import ItemsNeighborhoodStrategy


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Viewer')


base_api_url = "http://harrenhal-php-97705.apse1.nitrousbox.com/elgg/services/api/rest/json/"

def current_datetime(request):
    user_id = int(request.GET.get('user_id','287'))
    job = django_rq.enqueue(recommended,user_id)
    logger.debug(job.key)
    response_data = {'status':'processing', 'job': job.key}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    # return HttpResponse(job.key)

def get_result(request):
    job_id = request.GET.get('job_id')
    redis_conn = django_rq.get_connection()
    job_id=job_id.split(':')[2]
    logger.info(job_id)
    job = Job.fetch(job_id,redis_conn)
    if job.is_finished:
        ret = job.return_value
    elif job.is_queued:
        ret = {'status':'in-queue'}
    elif job.is_started:
        ret = {'status':'waiting'}
    elif job.is_failed:
        ret = {'status': 'failed'}
    return HttpResponse(json.dumps(ret), content_type="application/json")


@job
def recommended(user_id):
    payload = {'method': 'get.all.rating'}
    r = requests.get(base_api_url,params=payload)
    results = r.json()
    results = results['result']
    dataset = {}
    for result in results:
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
    return response_data
